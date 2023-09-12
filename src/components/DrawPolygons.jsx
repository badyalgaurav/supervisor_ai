// Example for draw polygon
//reference https://www.jsdelivr.com/package/npm/react-draw-polygons
import React, { useRef, useState, useEffect } from "react";
import CanvasPolygons, { POLYGON_SIZE, POLYGON_TYPE } from "react-draw-polygons";

const DrawPolygons = ({ cameraId }) => {
    const canvasRef = useRef();

    const defaultPoints = [{ "polygon": [{ "x": 465.20965591251695, "y": 153.624598516918 }, { "x": 354.9224184225682, "y": 96.19237876200808 }, { "x": 246.23161823749055, "y": 211.96072484645168 }, { "x": 343.4320077114818, "y": 409.98366363411947 }, { "x": 497.62540021763226, "y": 370.08526358368107 }], "label": "Label 1" }, { "polygon": [{ "x": 129.1745355192333, "y": 267.2255223916952 }, { "x": 81.42131184930514, "y": 330.38927044373355 }, { "x": 92.31819814153585, "y": 408.8194132970125 }, { "x": 155.48194619357415, "y": 456.57263696694054 }, { "x": 233.912089046853, "y": 445.6757506747099 }, { "x": 281.6653127167811, "y": 382.5120026226717 }, { "x": 270.76842642455046, "y": 304.0818597693926 }, { "x": 207.60467837251227, "y": 256.3286360994645 }], "label": "Label 2" }]

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


    const handleUpdate = () => {
        // @ts-ignore
        alert(JSON.stringify(canvasRef.current.onConfirm()))
    };
    const handleDrawRec = () => {
        // @ts-ignore
        canvasRef.current.onDraw({ type: POLYGON_TYPE.rec, size: POLYGON_SIZE.large });
    };

    const handleDrawHex = () => {
        // @ts-ignore
        canvasRef.current.onDraw({ type: POLYGON_TYPE.hex, size: POLYGON_SIZE.normal });
    };

    const handleDrawOct = () => {
        // @ts-ignore
        canvasRef.current.onDraw({ type: POLYGON_TYPE.oct, size: POLYGON_SIZE.small });
    };

    const handleDrawFree = () => {
        // @ts-ignore
        canvasRef.current.toggleDraw();
    };

    return (
        <div class="card d-flex flex-column h-100">
            <div class="card-header">
                <button style={{ marginRight: "5px" }} onClick={handleDrawRec}>Big Rectangle</button>
                <button style={{ marginRight: "5px" }} onClick={handleDrawHex}>Normal Hexagon</button>
                <button style={{ marginRight: "5px" }} onClick={handleDrawOct}>Small Octagon</button>
                <button style={{ marginRight: "5px" }} onClick={handleDrawFree}>Free Draw</button>
                <button style={{ marginRight: "5px" }} onClick={handleUpdate}>Get polygon</button>
            </div>
            <div class="card-body flex-grow-1 d-flex flex-column" style={{ padding:"0px" }}>
                <CanvasPolygons ref={canvasRef}  
                    defaultPolygons={polygons}
                    canvasHeight={458}
                    canvasWidth={812}
                    polygonStyle={{
                        fill: null,
                        strokeWidth: 2,
                        stroke: "green",
                        cornerColor: "blue",
                        cornerStyle: "circle",
                        cornerSize: 10,
                    }} >
                    <div                 
                    >
                        <img src={imageSrc} alt={`Camera ${cameraId}`} style={{ height: "458px", width: "812px" }} />
                    </div>
               
                </CanvasPolygons>
            </div>
        </div>
    );
}

export default DrawPolygons;