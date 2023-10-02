// Example for draw polygon
//reference https://www.jsdelivr.com/package/npm/react-draw-polygons
import React, { useRef, useState, useEffect, useContext } from "react";
import CanvasPolygons, { POLYGON_SIZE, POLYGON_TYPE } from "react-draw-polygons";
import { MainContextProvider } from "../utils/MainContextProvider";
const DashboardCamCard = ({ cameraId }) => {
    const contextData = useContext(MainContextProvider);
    const canvasRef = useRef();
    const polygons = [
        {
            polygon: [
                { x: 100, y: 100 },
                { x: 200, y: 100 },
                { x: 200, y: 200 },
                { x: 100, y: 200 }
            ]
        }
    ];
    //const polygons = [{ "polygon": [{ "x": 12.369884641415041, "y": 27.995807173017425 }, { "x": 408.60020994000314, "y": 27.995807173017425 }, { "x": 394.0000000000001, "y": 416.6757530325747 }, { "x": 8, "y": 421.6696197355868 }], "label": "Label 1" }]
    const [imageSrc, setImageSrc] = useState('');


    useEffect(() => {
        const socket = new WebSocket(`ws://localhost:8000/ws1/${cameraId}`);

        socket.binaryType = 'arraybuffer';

        socket.onmessage = function (event) {
            const imageUrl = URL.createObjectURL(new Blob([event.data], { type: 'image/jpeg' }));
            setImageSrc(imageUrl);
        };

        return () => {
            socket.close();
        };
    }, [cameraId]);

    const handleDrawFree = () => {
        // @ts-ignore
        canvasRef.current.toggleDraw();
    };
    // This function will be called whenever contextData changes
    useEffect(() => {
        // Execute your desired function here
        console.log('Context Data has changed:', contextData.updatePolygonStatus);
        if (contextData.updatePolygonStatus[parseInt(cameraId) - 1] == true) {
            canvasRef.current.toggleDraw();
        }

    }, [contextData]);
    return (
        <div class="card d-flex flex-column h-100">

            <div class="card-body flex-grow-1 d-flex flex-column" style={{ padding: "0px" }}>
                <CanvasPolygons ref={canvasRef}
                    defaultPolygons={polygons}
                    canvasHeight={512}
                    canvasWidth={812}
                    canEdit={contextData.updatePolygonStatus[parseInt(cameraId)-1]}
                    polygonStyle={{
                        fill: null,
                        strokeWidth: 2,
                        stroke: "green",
                        cornerColor: "blue",
                        cornerStyle: "circle",
                        cornerSize: 10,
                    }}>
                    <div> <img src={imageSrc} alt={`Camera ${cameraId}`} style={{ height: "512px", width: "812px" }} /> </div>
                </CanvasPolygons>
            </div>
        </div>
    );
}

export default DashboardCamCard;