import argparse
from collections import defaultdict, deque

import cv2
import numpy as np
from ultralytics import YOLO

# COCO ids:
# person=0, bicycle=1, car=2, motorcycle=3, bus=5, truck=7
# Si quieres también personas y bicis, cambia a: [0, 1, 2, 3, 5, 7]
VEHICLE_CLASSES = [0, 1, 2, 3, 5, 7]


def red_mask_hsv(bgr: np.ndarray, s_min: int, v_min: int) -> np.ndarray:
    """Máscara de rojo en HSV (rojo se parte en dos rangos)."""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

    lower1 = np.array([0,   s_min, v_min], dtype=np.uint8)
    upper1 = np.array([10,  255,   255], dtype=np.uint8)
    lower2 = np.array([170, s_min, v_min], dtype=np.uint8)
    upper2 = np.array([180, 255,   255], dtype=np.uint8)

    m1 = cv2.inRange(hsv, lower1, upper1)
    m2 = cv2.inRange(hsv, lower2, upper2)
    mask = cv2.bitwise_or(m1, m2)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    return mask


def find_stop_light_boxes(vehicle_roi: np.ndarray,
                          x0: int, y0: int,
                          bottom_frac: float,
                          s_min: int, v_min: int,
                          min_area: int,
                          max_area_frac: float,
                          min_solidity: float):
    """Busca blobs rojos en el % inferior del vehículo."""
    h, w = vehicle_roi.shape[:2]
    if h < 8 or w < 8:
        return [], None

    y_start = int(h * (1.0 - bottom_frac))
    roi = vehicle_roi[y_start:h, 0:w]
    if roi.size == 0:
        return [], None

    mask = red_mask_hsv(roi, s_min=s_min, v_min=v_min)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_area = int(roi.shape[0] * roi.shape[1] * max_area_frac)

    boxes = []
    for cnt in contours:
        area = float(cv2.contourArea(cnt))
        if area < min_area or area > max_area:
            continue

        hull = cv2.convexHull(cnt)
        hull_area = float(cv2.contourArea(hull)) if hull is not None else 0.0
        if hull_area > 0:
            solidity = area / hull_area
            if solidity < min_solidity:
                continue

        x, y, bw, bh = cv2.boundingRect(cnt)
        if bw <= 0 or bh <= 0:
            continue

        aspect = bw / float(bh)
        if aspect < 0.3 or aspect > 10.0:
            continue

        gx1 = x0 + x
        gy1 = y0 + y_start + y
        gx2 = gx1 + bw
        gy2 = gy1 + bh
        boxes.append((gx1, gy1, gx2, gy2, int(area)))

    return boxes, mask


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Video de entrada .mp4")
    ap.add_argument("--output", default="out_cars_stop.mp4", help="Video de salida .mp4")
    ap.add_argument("--model", default="yolo12n.pt", help="Modelo YOLO (ej: yolo12n.pt)")
    ap.add_argument("--tracker", default="bytetrack.yaml", help="bytetrack.yaml o botsort.yaml")
    ap.add_argument("--conf", type=float, default=0.25, help="Confianza YOLO")
    ap.add_argument("--trail", type=int, default=0, help="Longitud del trail (0 desactiva)")
    ap.add_argument("--bottom-frac", type=float, default=0.45, help="Zona inferior del coche a analizar (día: 0.40-0.55)")

    ap.add_argument("--s-min", type=int, default=85, help="S mínimo (día típico 70-120)")
    ap.add_argument("--v-min", type=int, default=70, help="V mínimo (día típico 60-110)")

    ap.add_argument("--min-area", type=int, default=60, help="Área mínima blob")
    ap.add_argument("--max-area-frac", type=float, default=0.08, help="Área máxima relativa por blob")
    ap.add_argument("--min-solidity", type=float, default=0.35, help="Solidity mínima (0.25-0.60)")

    ap.add_argument("--show", action="store_true", help="Muestra ventana en vivo")
    ap.add_argument("--show-mask", action="store_true", help="Muestra máscara del último vehículo (debug)")
    args = ap.parse_args()

    model = YOLO(args.model)
    names = model.names  # <- aquí están los nombres: {2:'car', 3:'motorcycle', ...}

    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        raise RuntimeError(f"No pude abrir: {args.input}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(args.output, fourcc, fps, (W, H))

    trails = defaultdict(lambda: deque(maxlen=max(args.trail, 1)))
    last_mask = None

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        results = model.track(
            source=frame,
            conf=args.conf,
            classes=VEHICLE_CLASSES,
            tracker=args.tracker,
            persist=True,
            verbose=False
        )

        out = frame.copy()

        r = results[0]
        if r.boxes is not None and r.boxes.id is not None:
            boxes_xyxy = r.boxes.xyxy.cpu().numpy().astype(int)
            ids = r.boxes.id.cpu().numpy().astype(int)
            confs = r.boxes.conf.cpu().numpy()
            clss = r.boxes.cls.cpu().numpy().astype(int)  # <- CLASES

            for (x1, y1, x2, y2), tid, cf, cls_id in zip(boxes_xyxy, ids, confs, clss):
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(W - 1, x2), min(H - 1, y2)
                if x2 <= x1 or y2 <= y1:
                    continue

                cls_name = names.get(int(cls_id), str(int(cls_id)))  # <- nombre

                if args.trail > 0:
                    cx = int((x1 + x2) / 2)
                    cy = int((y1 + y2) / 2)
                    trails[tid].append((cx, cy))

                vehicle_roi = frame[y1:y2, x1:x2]

                light_boxes, mask = find_stop_light_boxes(
                    vehicle_roi=vehicle_roi,
                    x0=x1, y0=y1,
                    bottom_frac=args.bottom_frac,
                    s_min=args.s_min,
                    v_min=args.v_min,
                    min_area=args.min_area,
                    max_area_frac=args.max_area_frac,
                    min_solidity=args.min_solidity
                )
                last_mask = mask

                # BBox vehículo + etiqueta con clase
                cv2.rectangle(out, (x1, y1), (x2, y2), (255, 255, 255), 1)
                cv2.putText(out, f"{cls_name} ID {tid}  {cf:.2f}", (x1, max(0, y1 - 6)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                # Luces stop
                for lx1, ly1, lx2, ly2, _area in light_boxes:
                    cv2.rectangle(out, (lx1, ly1), (lx2, ly2), (0, 255, 0), 2)
                    cv2.putText(out, "STOP", (lx1, max(0, ly1 - 6)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

        if args.trail > 0:
            for tid, pts in trails.items():
                if len(pts) < 2:
                    continue
                for i in range(1, len(pts)):
                    cv2.line(out, pts[i - 1], pts[i], (255, 0, 255), 2)

        writer.write(out)

        if args.show:
            cv2.imshow("Cars + Stop Lights", out)
            if args.show_mask and last_mask is not None:
                cv2.imshow("Red mask (vehicle bottom ROI)", last_mask)
            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q")):
                break

    cap.release()
    writer.release()
    if args.show:
        cv2.destroyAllWindows()
    print(f"Listo: {args.output}")


if __name__ == "__main__":
    main()
