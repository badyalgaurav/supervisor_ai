import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import NavbarCamCard from "../../components/NavbarCamCard"
import { apiSAIFrameworkAPIPath } from "../../config"
import Swal from "sweetalert2";


const Navbar = (props) => {
    const [data, setData] = useState("");
    const [cloudData, setCloudData] = useState([]);
    const [timeData, setTimeData] = useState("");
    const navigate = useNavigate();
    useEffect(() => {
        // Function to make an Axios request
        const fetchData = () => {
            const apiUrl = `${apiSAIFrameworkAPIPath}/alert/get_alert_counts/`;
            const requestData = {
                "user_id": localStorage.getItem("userId")
            };
            axios.get(apiUrl, {
                params: requestData
            })
                .then((response) => {
                    setData(response.data.data);
                })
                .catch((error) => {
                    console.error('Error fetching data:', error);
                });
        };
        const getTimeData = () => {
            const apiUrl = `${apiSAIFrameworkAPIPath}/geofence/get_time_data/`;
            const requestData = {
                "user_id": localStorage.getItem("userId")
            };
            axios.get(apiUrl, {
                params: requestData
            })
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

    const handleLogout = () => {
        Swal.fire({
            title: 'Are you sure?',
            text: 'You want to logout!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes!'
        }).then((result) => {
            if (result.isConfirmed) {
                // Handle the deletion logic here
                Swal.fire('Logout!', 'you are successfully logout.', 'success');

                localStorage.clear();
               
                navigate('/Login');
            }
        });
    }

    return (
        <>
            <div className={`sidebar pb-3 ${props.isOpen ? 'open' : ''}`}>
                <nav class="navbar bg-secondary navbar-dark">
                    <div href="" class="navbar-brand mx-4 mb-3">
                        <h3 class="text-primary">SafetyEyePro <span class="text-default text-right" style={{color:"white"}}><i class="fa fa-power-off" aria-hidden="true" onClick={handleLogout }></i></span></h3>
                        

                    </div>
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