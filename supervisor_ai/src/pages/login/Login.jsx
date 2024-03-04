import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiSAIFrameworkAPIPath } from "../../config"
import Swal from "sweetalert2";
import axios from 'axios';

const Login = () => {
    const navigate = useNavigate();
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
                    localStorage.setItem("aiPerSecond", response.data.aiPerSecondRatio);
                    localStorage.setItem("cameraInfo", JSON.stringify(response.data.cameraInfo));

                    Swal.fire({
                        icon: "success",
                        title: "Sucess!",
                        text: "Successfully logged in.",
                    });
                    navigate('/');
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
                                    <h3 class="text-primary"><i class="fa fa-user-edit me-2"></i>Safety eye pro</h3>
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