import React, { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';

import Header from "../../components/common/Header";
import Navbar from "../../components/common/Navbar";
const Layout = () => {
    const [showSpinner, setShowSpinner] = useState(true);

    useEffect(() => {
        // Show the spinner initially
        setShowSpinner(true);

        // Set a timeout to hide the spinner after the delay
        const timeoutId = setTimeout(() => {
            setShowSpinner(false);
        }, 1);

        // Clean up the timeout when the component unmounts or when the effect is re-run
        return () => clearTimeout(timeoutId);
    }, []); // The empty array [] ensures the effect runs only once after the initial render

    return (
        <div>
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
                <Navbar />
               
                <div class="content">
                    <Header />

                    <div class="">
                     
                        <div class="container-fluid pt-2 px-2">
                            <Outlet />
                        </div>
                    </div>
                </div>
                {/* <Footer /> */}
            </div>
        </div>
    );
};

export default Layout;