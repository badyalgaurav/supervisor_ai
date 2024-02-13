import React, { useEffect, useState } from "react";
import axios from 'axios';
import NavbarCamCard from "../../components/NavbarCamCard"
import { apiSAIFrameworkAPIPath } from "../../config"



const Navbar = (props) => {
    const [data, setData] = useState("");
    const [cloudData, setCloudData] = useState([]);
    const [timeData, setTimeData] = useState("");

    useEffect(() => {
        // Function to make an Axios request
        const fetchData = () => {
            const apiUrl = `${apiSAIFrameworkAPIPath}/mongo_op/get_alert_counts/`;
            axios.get(apiUrl)
                .then((response) => {
                    setData(response.data.data);
                })
                .catch((error) => {
                    console.error('Error fetching data:', error);
                });
        };
        const getTimeData = () => {
            const apiUrl = `${apiSAIFrameworkAPIPath}/mongo_op/get_time_data/`;
            axios.get(apiUrl)
                .then((response) => {
                    setTimeData(response.data.data);
                }) .catch((error) => {
                    console.error('Error fetching data:', error);
                });
        };

        // Initial request when the component mounts
        fetchData();
        getTimeData();
        // Set up a recurring request every one minute (60000 milliseconds)
        const interval = setInterval(() => {
            fetchData();
        }, 10 * 1000);

        // Clear the interval when the component is unmounted to prevent memory leaks
        return () => {
            clearInterval(interval);
        };
    }, []); // Empty dependency array means this effect runs once when the component mounts


    const loadInit = () => {
        if (localStorage.getItem("cameraInfo")) {
            // Set the data and update the loading state
            const result = JSON.parse(localStorage.getItem("cameraInfo"))
            //const response = updateDimensions(result);
            setCloudData(result);
        }
        
    }

    useEffect(() => {
        loadInit();
    }, []);


    return (
        <>
            <div className={`sidebar pb-3 ${props.isOpen ? 'open' : ''}`}>
                <nav class="navbar bg-secondary navbar-dark">
                    <a href="index.html" class="navbar-brand mx-4 mb-3">
                        <h3 class="text-primary">SafetyEyePro</h3>
                    </a>
                    <div class="navbar-nav w-100">
                        <div class="nav-item dropdown">

                           
                                {/*Map over the data and render each item*/}
                                {cloudData?.map((item) => (
                                    <div>
                                        <NavbarCamCard camNo={item.displayOrder} data={data} timeData={timeData}></NavbarCamCard>
                                        {/*<DashboardCamCard cameraId={item.displayOrder} height={item.height} width={item.width} connString={item.connectionString}></DashboardCamCard>*/}
                                    </div>


                                ))}
                           


                            {/*<div className="">*/}
                            {/*    <NavbarCamCard camNo={"1"} data={data} timeData={timeData}></NavbarCamCard>*/}
                            {/*</div>*/}

                            {/*<div className="">*/}
                            {/*    <NavbarCamCard camNo={"2"} data={data} timeData={timeData}></NavbarCamCard>*/}
                            {/*</div>*/}
                            {/*<div className="">*/}
                            {/*    <NavbarCamCard camNo={"3"} data={data} timeData={timeData}></NavbarCamCard>*/}
                            {/*</div>*/}
                            {/*<div className="">*/}
                            {/*    <NavbarCamCard camNo={"4"} data={data} timeData={timeData}></NavbarCamCard>*/}
                            {/*</div>*/}
                        </div>
                    </div>
                </nav>
            </div>
        </>)
};
export default Navbar;