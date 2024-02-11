import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import DashboardCamCard from '../../components/DashboardCamCard';
import { apiGemmiz } from "../../config"
import axios from 'axios';

const Dashboard = () => {
    const [data, setData] = useState(null);
    const [divClass, setDivClass] = useState("col-md-6");
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();
    const getDimensions = (noOfCameras) => {
        let response = { "height": 534, "width": 812 }
        switch (noOfCameras) {
            case 1:
                setDivClass("")
                response["height"] = 1068
                response["width"] = 1624
                break;
            case 2:
                response["height"] = 1068
                break;

            default:
                return response;
        }
        return response;

    }
    const updateDimensions = (data) => {
        const response = getDimensions(data.length)
        const updatedData = data.map(item => {
            item["height"] = response.height;
            item["width"] = response.width;
            return item; // Don't forget to return the modified item
        });
        return updatedData;

    }

    const loadInit = () => {
        if (localStorage.getItem("cameraInfo")) {
            debugger;
            // Set the data and update the loading state
            const result = JSON.parse(localStorage.getItem("cameraInfo"))
            const response = updateDimensions(result);
            setData(response);
            setLoading(false);
        }
        else {
            alert("Stored information expired.please login again.");
            navigate('/Login');
        }
    }

    useEffect(() => {
        loadInit();
    }, []);


    return (
        <><div class="row bg-secondary mx-0">
            {/*<div class="col-md-6">*/}
            {/*    <DashboardCamCard cameraId={"1"}></DashboardCamCard>*/}
            {/*</div>*/}
            {/*<div class="col-md-6">*/}
            {/*    <DashboardCamCard cameraId={"2"}></DashboardCamCard>*/}
            {/*</div>*/}
            {/*<div class="col-md-6">*/}
            {/*    <DashboardCamCard cameraId={"3"}></DashboardCamCard>*/}
            {/*</div>*/}
            {/*<div class="col-md-6">*/}
            {/*    <DashboardCamCard cameraId={"4"}></DashboardCamCard>*/}
            {/*</div>*/}
            {loading ? (
                <p>Loading...</p>
            ) : (
                <>
                    {/*Map over the data and render each item*/}
                        {
                            data.map((item) => (
                        <div class={divClass}>
                            <DashboardCamCard cameraId={item.displayOrder} height={item.height} width={item.width} connString={item.connectionString}></DashboardCamCard>
                        </div>
                    ))}
                </>
            )}
        </div></>
    );
};

export default Dashboard;