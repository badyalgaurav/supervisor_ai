import React, { useEffect, useRef, useState } from 'react';

const samplePolygon = [
    { x: 100, y: 100 },
    { x: 300, y: 100 },
    { x: 300, y: 300 },
    { x: 100, y: 300 }
];

const PolygonCameraStream = ({ cameraId }) => {
    const imageRef = useRef(null);
    const canvasRef = useRef(null);
    const [drawing, setDrawing] = useState(false);
    const [points, setPoints] = useState([]);

    useEffect(() => {
        const socket = new WebSocket(`ws://localhost:8000/ws/${cameraId}`);
        socket.binaryType = 'arraybuffer';

        socket.onmessage = function (event) {
            const imageUrl = URL.createObjectURL(new Blob([event.data], { type: 'image/jpeg' }));
            imageRef.current.src = imageUrl;
        };

        return () => {
            socket.close();
        };
    }, [cameraId]);

    useEffect(() => {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.drawImage(imageRef.current, 0, 0);

        if (samplePolygon) {
            drawPolygon(context, samplePolygon); // Draw the preset polygon
        }

        if (drawing) {
            drawPolygon(context, points);
        }
    }, [points, drawing]);

    const handleCanvasMouseDown = (event) => {
        setDrawing(true);
        const newPoint = { x: event.nativeEvent.offsetX, y: event.nativeEvent.offsetY };
        setPoints([...points, newPoint]);
    };

    const handleCanvasMouseMove = (event) => {
        if (!drawing) return;
        const newPoint = { x: event.nativeEvent.offsetX, y: event.nativeEvent.offsetY };
        setPoints([...points, newPoint]);
    };

    const handleCanvasMouseUp = () => {
        setDrawing(false);
    };

    const drawPolygon = (context, points) => {
        if (points.length < 2) return;

        context.beginPath();
        context.moveTo(points[0].x, points[0].y);
        for (let i = 1; i < points.length; i++) {
            context.lineTo(points[i].x, points[i].y);
        }
        context.strokeStyle = 'red';
        context.lineWidth = 2;
        context.stroke();
    };

    return (
        <div style={{ position: 'relative' }}>
            <img
                ref={imageRef}
                alt={`Camera ${cameraId}`}
                style={{ width: '100%' }}
            />
            <canvas
                ref={canvasRef}
                onMouseDown={handleCanvasMouseDown}
                onMouseMove={handleCanvasMouseMove}
                onMouseUp={handleCanvasMouseUp}
                style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none' }}
            />
        </div>
    );
};

export default PolygonCameraStream;
