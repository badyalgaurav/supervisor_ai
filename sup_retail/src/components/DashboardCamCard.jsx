// Example for draw polygon
//reference https://www.jsdelivr.com/package/npm/react-draw-polygons
import React, { useRef, useState, useEffect, useContext } from "react";
import { useNavigate } from 'react-router-dom';
import FabricJSCanvas from "../components/fabricJs/FabricJSCanvas"
import { apiWebSocketPath } from "../config"
const DashboardCamCard = ({ userId, cameraId, height, width, connString, aiPerSecondRatio }) => {
    const navigate = useNavigate();
    const handleImageErro = () => {
        console.log("frames are empty for this camera.");
        alert("Camera is not connected or Service is stopped. Please check and log in again.");
        navigate('/login');
    }

    return (
        <div class="card d-flex flex-column h-100">
            <div class="card-body flex-grow-1 d-flex flex-column" style={{ padding: "0px" }}>
                <div style={{ position: 'relative', width: `${width}px`, height: `${height}px` }}>
                    <div style={{ position: 'absolute', top: 0, left: 0 }}>
                        {/*<img*/}
                        {/*    src="https://picsum.photos/seed/picsum/200/300"*/}
                        {/*    style={{ height: '534px', width: '812px' }}*/}
                        {/*/>*/}
                        <img src={`${apiWebSocketPath}/video_feed?user_id=${userId}&camera_id=${cameraId}&conn_str=${connString}&height=${height}&width=${width}&ai_per_second=${aiPerSecondRatio}`} alt={`Camera ${cameraId}`} style={{ width: `${width}px`, height: `${height}px` }} onError={handleImageErro } />
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