import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiSAIFrameworkAPIPath, apiWebSocketPath } from "../../config"
import Swal from "sweetalert2";
import axios from 'axios';

const Login = () => {
    const navigate = useNavigate();

    const getDimensions = (noOfCameras) => {
        let response = { "height": 534, "width": 812 }
        switch (noOfCameras) {
            case 1:
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
        const response = getDimensions(data.length);
        const updatedData = data.map(item => {
            item["height"] = response.height;
            item["width"] = response.width;
            return item;
        });
        return updatedData;
    }

    const handleInitAPI = (data) => {
        debugger;
        const apiUrl = `${apiWebSocketPath}/init_api/`;
        data.cameraInfo = updateDimensions(data.cameraInfo);

        data.cameraInfo.forEach((camera) => {
            debugger;
            const requestData = {
                "user_id": data._id,
                "camera_id": camera.displayOrder,
                "conn_str": camera.connectionString,
                "height": camera.height, // Update height based on response
                "width": camera.width,   // Update width based on response
                "ai_per_second": localStorage.getItem("aiPerSecondRatio")
            };
            //axios.get(apiUrl, { params: requestData })
            axios.post(apiUrl, requestData)
                .then((response) => {
                    console.log("API initialized successfully");
                })
                .catch((error) => {
                    console.error("Error while initializing API", error);
                });
        });
    }
    const handleLogin = () => {
        var email = document.querySelector('#txtEmail').value;
        var password = document.querySelector('#txtPassword').value;
        const apiUrl = `${apiSAIFrameworkAPIPath}/gemmiz/get_camera_credentials`; // Replace with your API endpoint URL
        const requestData = {
            "email": email,
            "password": password
        };

        axios.get(apiUrl, { params: requestData })
            .then((response) => {
                if (response.data) {
                    localStorage.setItem("userId", response.data._id);
                    localStorage.setItem("email", response.data.cEmail);
                    localStorage.setItem("aiPerSecondRatio", response.data.aiPerSecondRatio !== undefined ? response.data.aiPerSecondRatio : 8);
                    localStorage.setItem("cameraInfo", JSON.stringify(response.data.cameraInfo));
                    handleInitAPI(response.data);

                    setTimeout(() => {
                        Swal.fire({
                            icon: "success",
                            title: "Sucess!",
                            text: "Successfully logged in.",
                        });
                        navigate('/');
                    }, 3000);

                }
                else {

                    Swal.fire({
                        icon: "warning",
                        title: "wrong credentials!",
                        text: "You have entered wrong email or password. Try again!",
                    });
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    return (<>
        <div class="container-fluid position-relative d-flex p-0">
            <div class="container-fluid">
                <div class="row h-100 align-items-center justify-content-center" >
                    <div class="col-12 col-sm-8 col-md-6 col-lg-5 col-xl-4">
                        <div class="bg-secondary rounded p-4 p-sm-5 my-4 mx-3">
                            <div class="d-flex align-items-center justify-content-between mb-3">
                                <a href="index.html" class="">
                                    <h3 class="text-primary"><i class="fa fa-user me-2"></i>AI eye pro</h3>
                                </a>
                                <h3>Sign In</h3>
                            </div>
                            <div class="form-floating mb-3">
                                <input type="email" class="form-control" id="txtEmail" placeholder="name@example.com"></input>
                                <label for="floatingInput">Email address</label>
                            </div>
                            <div class="form-floating mb-4">
                                <input type="password" class="form-control" id="txtPassword" placeholder="Password"></input>
                                <label for="floatingPassword">Password</label>
                            </div>
                            <button type="button" onClick={handleLogin} class="btn btn-primary py-3 w-100 mb-4">Sign In</button>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </>);
};

export default Login;