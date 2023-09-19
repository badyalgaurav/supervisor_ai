import React, { useEffect, useRef } from "react";
import DashboardCamCard from '../../components/DashboardCamCard';
import DashboardCamCardSetting from "../../components/DashboardCamCardSetting";
const Dashboard = () => {
    return (<>
        <div class="row bg-secondary rounded align-items-center justify-content-center mx-0">
            <div class="col-md-6 camera_card camera_right_padding">
                <DashboardCamCardSetting cameraId={0}></DashboardCamCardSetting>
            </div>
            <div class="col-md-6 camera_card camera_left_padding">
                <DashboardCamCard cameraId={0}></DashboardCamCard>
            </div>
            <div class="col-md-6  camera_card camera_right_padding">
                <DashboardCamCard cameraId={0}></DashboardCamCard>
            </div>
            <div class="col-md-6 camera_card camera_left_padding">
                <DashboardCamCard cameraId={0}></DashboardCamCard>
            </div>
        </div>
    </>);
};

export default Dashboard;