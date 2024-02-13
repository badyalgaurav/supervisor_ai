// Example for draw polygon
//reference https://www.jsdelivr.com/package/npm/react-draw-polygons
import React, { useRef, useState, useEffect, useContext } from "react";
//import axios from 'axios';
//import Swal from "sweetalert2";
import FabricJSCanvas from "../components/fabricJs/FabricJSCanvas"
//import { MainContextProvider } from "../utils/MainContextProvider";
//import { apiSAIFrameworkAPIPath, apiWebSocketPath } from "../config"
const DashboardCamCard = ({ cameraId, height,width, connString }) => {
    debugger;
    //const contextData = useContext(MainContextProvider);
    //const canvasRef = useRef();
    //const polygons = JSON.parse(localStorage.getItem(`polyFor_${cameraId}`));//contextData.polygonInfo;
    //const showSuccessAlert = () => {
    //    Swal.fire({
    //        icon: "success",
    //        title: "Saved!",
    //        text: "Your changes have been successfully saved.",
    //    });
    //};

    //const handSavePolygon = (cameraId, polygonInfo) => {
        
    //    const apiUrl = `${apiSAIFrameworkAPIPath}/mongo_op/upsert_polygon/`; 
    //    const requestData = {
    //        "camera_no": parseInt(cameraId),
    //        "polygon_info": polygonInfo,
    //    };

    //    axios.post(apiUrl, requestData)
    //        .then((response) => {
    //            // Handle the successful response here
    //            console.log('Response data:', response.data);
    //            showSuccessAlert();
    //        })
    //        .catch((error) => {
    //            // Handle any errors that occurred during the request
    //            console.error('Error:', error);
    //        });
    //}

    // This function will be called whenever contextData changes
    //useEffect(() => {
        
    //    // Execute your desired function here
    //    console.log('Context Data has changed:', contextData.updatePolygonStatus);
    //    if (contextData.updatePolygonStatus[parseInt(cameraId) - 1] == true) {
    //        canvasRef.current.toggleDraw();
    //    }
    //    if (contextData.savePolygonStatus[parseInt(cameraId) - 1] == true) {
    //        //alert(JSON.stringify(canvasRef.current.onConfirm()))
    //        contextData.savePolygonStatusFn(false, cameraId)
    //        handSavePolygon(cameraId, JSON.stringify(canvasRef.current.onConfirm()))
    //    }

    //}, [contextData]);


    return (
        <div class="card d-flex flex-column h-100">
            <div class="card-body flex-grow-1 d-flex flex-column" style={{ padding: "0px" }}>
                <div style={{ position: 'relative', width: `${width}px`, height: `${height}px` }}>
                    <div style={{ position: 'absolute', top: 0, left: 0 }}>
                        {/*<img*/}
                        {/*    src="https://picsum.photos/seed/picsum/200/300"*/}
                        {/*    style={{ height: '534px', width: '812px' }}*/}
                        {/*/>*/}
                        <img src={`http://127.0.0.1:8000/video_feed?camera_id=${cameraId}&conn_str=${connString}&height=${height}&width=${width}`} alt={`Camera ${cameraId}`} style={{ width: `${width}px`, height: `${height}px` }} />
                    </div>
                    <div style={{ position: 'absolute', top: 0, left: 0 }}>
                        <FabricJSCanvas cameraId={cameraId} height={height} width={width} />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default DashboardCamCard;