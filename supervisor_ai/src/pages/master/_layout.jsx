import React, { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';

import Header from "../../components/common/Header";
import Navbar from "../../components/common/Navbar";
import axios from 'axios';
import { apiSAIFrameworkAPIPath, apiWebSocketPath } from "../../config"
import { MainContextProvider } from "../../utils/MainContextProvider";
const Layout = () => {
    //const initPolygonStatus = { "cam_1": false, "cam_2": false, "cam_3": false, "cam_4": false}
    const [enableEditingPolygonStatus, setEnableEditingPolygonStatus] = useState([false, false, false, false]);
    const [polygonInfo, setPolygonInfo] = useState([false, false, false, false]);
    const [timeVal, setTimeVal] = useState([false, false, false, false]);
    const [savePolygonStatus, setSaveePolygonStatus] = useState([false, false, false, false]);
    const [deleteActivePolygonStatus, setDeleteActivePolygonStatus] = useState([false, false, false, false]);
    const [resetStatus, setResetStatus] = useState([false, false, false, false]);
    const [addPolygonStatus, setAddPolygonStatus] = useState([false, false, false, false]);
    const [addRecPolygonStatus, setAddRecPolygonStatus] = useState([false, false, false, false]);
    const [showSpinner, setShowSpinner] = useState(true);
    const [isOpen, setIsOpen] = useState(false);

    const initCamera = () => {
        setShowSpinner(true);
        const apiUrl = `${apiWebSocketPath}/camera_startup/`;
        axios.get(apiUrl)
            .then((response) => {
                debugger;
                if (response.data == "loading") {
                    setTimeout(() => {
                        initCamera();
                    }, 1000);
                }
                else {
                    setShowSpinner(false);
                }
                
            })
            .catch((error) => {
                console.error('Error fetching data:', error);
            });
    };

  
   
  
    useEffect(() => {
        // Show the spinner initially
        setShowSpinner(true);
        initCamera();
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


    const enableEditingPolygonStatusFn = (newValue, camNo) => {
        setEnableEditingPolygonStatus(prevState => {
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

    const deleteActivePolygonStatusFn = (newValue, camNo) => {
        setDeleteActivePolygonStatus(prevState => {
            // Create a copy of the existing state array
            const currentDeletePolygonStatus = [false, false, false, false];

            // Update the copy with the new value at the specified index
            currentDeletePolygonStatus[parseInt(camNo) - 1] = newValue;

            // Return the modified copy as the new state
            return currentDeletePolygonStatus;
        });
    };

    const resetStatusFn = (newValue, camNo) => {
        setResetStatus(prevState => {
            // Create a copy of the existing state array
            const currentResetStatus = [false, false, false, false];

            // Update the copy with the new value at the specified index
            currentResetStatus[parseInt(camNo) - 1] = newValue;

            // Return the modified copy as the new state
            return currentResetStatus;
        });
    };

    const addPolygonStatusFn = (newValue, camNo) => {
        setAddPolygonStatus(prevState => {
            // Create a copy of the existing state array
            const currentAddPolygonStatus = [false, false, false, false];

            // Update the copy with the new value at the specified index
            currentAddPolygonStatus[parseInt(camNo) - 1] = newValue;

            // Return the modified copy as the new state
            return currentAddPolygonStatus;
        });
    };
    const addRecPolygonStatusFn = (newValue, camNo) => {
        setAddRecPolygonStatus(prevState => {
            // Create a copy of the existing state array
            const currentAddRecPolygonStatus = [false, false, false, false];

            // Update the copy with the new value at the specified index
            currentAddRecPolygonStatus[parseInt(camNo) - 1] = newValue;

            // Return the modified copy as the new state
            return currentAddRecPolygonStatus;
        });
    };
    //useEffect(() => {
    //    // Show the spinner initially
    //    setShowSpinner(true);
    //    handleGetPolygon(3)
    //    // Set a timeout to hide the spinner after the delay
    //    const timeoutId = setTimeout(() => {
    //        setShowSpinner(false);
    //    }, 1);

    //    // Clean up the timeout when the component unmounts or when the effect is re-run
    //    return () => clearTimeout(timeoutId);
    //}, []); 
    return (
        <div>
            <MainContextProvider.Provider value={{
                enableEditingPolygonStatus,  enableEditingPolygonStatusFn,
                savePolygonStatus, savePolygonStatusFn,
                deleteActivePolygonStatus, deleteActivePolygonStatusFn,
                resetStatus, resetStatusFn,
                addPolygonStatus, addPolygonStatusFn,
                addRecPolygonStatus, addRecPolygonStatusFn,
                polygonInfo,
                timeVal, setTimeVal
            }}>
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