import React, { useEffect, useRef } from "react";
import DrawPolygons from '../../components/DrawPolygons';
const Dashboard = () => {
    return (<>
        <div class="row bg-secondary rounded align-items-center justify-content-center mx-0">

            <div class="col-md-6 camera_card">
                <DrawPolygons cameraId={0}></DrawPolygons>
            </div>
            <div class="col-md-6 camera_card">

                <DrawPolygons cameraId={0}></DrawPolygons>

            </div>
            <div class="col-md-6  camera_card">

                <DrawPolygons cameraId={0}></DrawPolygons>

            </div>
            <div class="col-md-6 camera_card">

                <DrawPolygons cameraId={0}></DrawPolygons>

            </div>
        </div>
    </>);
};

export default Dashboard;