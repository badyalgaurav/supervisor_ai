import React, { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';

import Header from "../../components/common/Header";
import Navbar from "../../components/common/Navbar";
import axios from 'axios';
import { apiSAIFrameworkAPIPath, apiWebSocketPath } from "../../config"
import { MainContextProvider } from "../../utils/MainContextProvider";
const Layout = () => {
    //const initPolygonStatus = { "cam_1": false, "cam_2": false, "cam_3": false, "cam_4": false}
    const [updatePolygonStatus, setUpdatePolygonStatus] = useState([false, false, false, false]);
    const [polygonInfo, setPolygonInfo] = useState([false, false, false, false]);
    const [savePolygonStatus, setSaveePolygonStatus] = useState([false, false, false, false]);
    const [showSpinner, setShowSpinner] = useState(true);
    const [isOpen, setIsOpen] = useState(false);

    const handleGetPolygon = (cameraId) => {
        const apiUrl = `${apiSAIFrameworkAPIPath}/mongo_op/get_polygon`; // Replace with your API endpoint URL
        const requestData = {
            // "camera_no": parseInt(cameraId)

        };

        axios.get(apiUrl, {
            params: requestData
        })
            .then((response) => {
                const responseData = response.data.data;
                for (let i = 0; i < responseData.length; i++) {
                    const item = responseData[i];
                    localStorage.setItem(`polyFor_${item.camera_no}`, JSON.stringify(item.polygonInfo))
                    // Process each item in the response data here
                }
            })
            .catch((error) => {
                // Handle any errors that occurred during the request
                console.error('Error:', error);
            });
    }

    useEffect(() => {
        // Show the spinner initially
        setShowSpinner(true);
        handleGetPolygon(3)
        // Set a timeout to hide the spinner after the delay
        const timeoutId = setTimeout(() => {
            setShowSpinner(false);
        }, 1);

        // Clean up the timeout when the component unmounts or when the effect is re-run
        return () => clearTimeout(timeoutId);
    }, []); // The empty array [] ensures the effect runs only once after the initial render

    const toggleSidebar = () => {
        setIsOpen(!isOpen);
    };


    const updatePolygonStatusFn = (newValue, camNo) => {
        setUpdatePolygonStatus(prevState => {
            // Create a copy of the existing state array
            const currentPolygonStatus = [...prevState];

            // Update the copy with the new value at the specified index
            currentPolygonStatus[parseInt(camNo) - 1] = newValue;

            // Return the modified copy as the new state
            return currentPolygonStatus;
        });
    };

    const savePolygonStatusFn = (newValue, camNo) => {
        setSaveePolygonStatus(prevState => {
            // Create a copy of the existing state array
            const currentPolygonStatus = [false, false, false, false];

            // Update the copy with the new value at the specified index
            currentPolygonStatus[parseInt(camNo) - 1] = newValue;

            // Return the modified copy as the new state
            return currentPolygonStatus;
        });
    };

    return (
        <div>
            <MainContextProvider.Provider value={{ updatePolygonStatus, updatePolygonStatusFn, savePolygonStatus, savePolygonStatusFn, polygonInfo }}>
                <div class="container-fluid position-relative d-flex p-0">
                    {/*<!-- Spinner Start -->*/}
                    <div
                        id="spinner"
                        className={`bg-dark position-fixed translate-middle w-100 vh-100 top-50 start-50 d-flex align-items-center justify-content-center ${showSpinner ? 'show' : ''
                            }`}
                    >
                        <div className="spinner-border text-primary" style={{ width: "10rem", height: "10rem" }} role="status">
                            <span className="sr-only">Loading...</span>
                        </div>
                    </div>
                    {/*<!-- Spinner End -->*/}
                    <Navbar isOpen={isOpen} />

                    <div className={`content ${isOpen ? 'open' : ''}`}>
                        {/*<Header toggleSidebar={toggleSidebar} />*/}

                        <div class="">

                            <div class="container-fluid px-2">
                                <Outlet />
                            </div>
                        </div>
                    </div>
                    {/* <Footer /> */}
                </div>
            </MainContextProvider.Provider>
        </div>
    );
};

export default Layout;