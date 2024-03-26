// Example for draw polygon
//reference https://www.jsdelivr.com/package/npm/react-draw-polygons
import React, { useRef, useState, useEffect, useContext } from "react";
import axios from 'axios';
import Swal from "sweetalert2";
import CanvasPolygons, { POLYGON_SIZE, POLYGON_TYPE } from "react-draw-polygons";
import { MainContextProvider } from "../utils/MainContextProvider";
import { apiSAIFrameworkAPIPath, apiWebSocketPath } from "../config"
const DashboardCamCard = ({ cameraId }) => {
 
    
    const contextData = useContext(MainContextProvider);
    const canvasRef = useRef();
    const polygons = JSON.parse(localStorage.getItem(`polyFor_${cameraId}`));//contextData.polygonInfo;
    //[
    //    {
    //        polygon: [
    //            { x: 100, y: 100 },
    //            { x: 200, y: 100 },
    //            { x: 200, y: 200 },
    //            { x: 100, y: 200 }
    //        ]
    //    }
    //];
    //const polygons = [{ "polygon": [{ "x": 12.369884641415041, "y": 27.995807173017425 }, { "x": 408.60020994000314, "y": 27.995807173017425 }, { "x": 394.0000000000001, "y": 416.6757530325747 }, { "x": 8, "y": 421.6696197355868 }], "label": "Label 1" }]
    const [imageSrc, setImageSrc] = useState('');


    //useEffect(() => {
    //    //handleGetPolygon(cameraId)
    //    console.log("socket useeffect")
    //    const socket = new WebSocket(`ws://localhost:8000/ws1/${cameraId}`);

    //    socket.binaryType = 'arraybuffer';

    //    socket.onmessage = function (event) {
    //        const imageUrl = URL.createObjectURL(new Blob([event.data], { type: 'image/jpeg' }));
    //        setImageSrc(imageUrl);
    //    };

    //    return () => {
    //        socket.close();
    //    };
    //}, [cameraId]);
    const showSuccessAlert = () => {
        Swal.fire({
            icon: "success",
            title: "Saved!",
            text: "Your changes have been successfully saved.",
        });
    };

    const handSavePolygon = (cameraId, polygonInfo) => {
        
        const apiUrl = `${apiSAIFrameworkAPIPath}/mongo_op/upsert_polygon/`; 
        const requestData = {
            "camera_no": parseInt(cameraId),
            "polygon_info": polygonInfo,
        };

        axios.post(apiUrl, requestData)
            .then((response) => {
                // Handle the successful response here
                console.log('Response data:', response.data);
                showSuccessAlert();
            })
            .catch((error) => {
                // Handle any errors that occurred during the request
                console.error('Error:', error);
            });
    }

    // This function will be called whenever contextData changes
    useEffect(() => {
        
        // Execute your desired function here
        console.log('Context Data has changed:', contextData.updatePolygonStatus);
        if (contextData.updatePolygonStatus[parseInt(cameraId) - 1] == true) {
            canvasRef.current.toggleDraw();
        }
        if (contextData.savePolygonStatus[parseInt(cameraId) - 1] == true) {
            //alert(JSON.stringify(canvasRef.current.onConfirm()))
            contextData.savePolygonStatusFn(false, cameraId)
            handSavePolygon(cameraId, JSON.stringify(canvasRef.current.onConfirm()))
        }

    }, [contextData]);


    return (
        <div class="card d-flex flex-column h-100">

            <div class="card-body flex-grow-1 d-flex flex-column" style={{ padding: "0px" }}>
                <CanvasPolygons ref={canvasRef}
                    defaultPolygons={polygons}
                    canvasHeight={534}
                    canvasWidth={812}
                    canEdit={contextData.updatePolygonStatus[parseInt(cameraId)-1]}
                    polygonStyle={{
                        fill: null,
                        strokeWidth: 4,
                        stroke: "yellow",
                        cornerColor: "blue",
                        cornerStyle: "circle",
                        cornerSize: 10,
                    }}>
                    {/*<div> <img src={imageSrc} alt={`Camera ${cameraId}`} style={{ height: "534px", width: "812px" }} /> </div>*/}
                    <div> <img src={`${apiWebSocketPath}/video_feed?camera_id=${cameraId}`} alt={`Camera ${cameraId}`} style={{ height: "534px", width: "812px" }} /> </div>
                </CanvasPolygons>
            </div>
        </div>
    );
}

export default DashboardCamCard;