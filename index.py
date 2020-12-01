# run  pip3 install opencv-contrib-python
import cv2
import argparse


def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 3)


def run(video, output, frame_number, xx, xy, yy, yx):
    tracker = cv2.TrackerMOSSE_create()
    cap = cv2.VideoCapture(video)
    # TRACKER INITIALIZATION
    cap.set(1, float(frame_number))
    success, start_frame = cap.read()
    bbox = (int(xx), int(xy), int(yy), int(yx))
    tracker.init(start_frame, bbox)
    cap.set(1, float(0))

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(output, fourcc, 20.0, (int(width), int(height)))

    while (cap.isOpened()):
        ret, frame = cap.read()

        if ret == True:
            success, bbox = tracker.update(frame)

            if success:
                drawBox(frame, bbox)

            out.write(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def main():
    run(args['video'], args['output'], args['frame'], args['xx'], args['xy'], args['yy'], args['yx'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument('-v', '--video',
                        help='Input video file path (source)',
                        required=True)
    parser.add_argument('-o', '--output',
                        help='Output video file path',
                        required=True)
    parser.add_argument('-f', '--frame',
                        help='Input vide frame',
                        required=True)
    parser.add_argument('-xx', '--xx',
                        help='Selection object box xx',
                        required=True)
    parser.add_argument('-xy', '--xy',
                        help='Selection object box xy',
                        required=True)
    parser.add_argument('-yy', '--yy',
                        help='Selection object box yy',
                        required=True)
    parser.add_argument('-yx', '--yx',
                        help='Selection object box yx',
                        required=True)
    args = vars(parser.parse_args())
    main()
