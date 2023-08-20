import React, { useEffect, useState } from "react";

const Dashboard = () => {
    return (<>
        <div class="row bg-secondary rounded align-items-center justify-content-center mx-0">
          
            <div class="col-md-6 text-center camera_card">
                <div class="card camera_card d-flex flex-column h-100">
                    <div class="card-header">Camera 1</div>
                    <div class="card-body flex-grow-1 d-flex flex-column justify-content-center">
                        <h3 class="text-center">This is a blank page</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-6 camera_card text-center">
                <div class="card camera_card d-flex flex-column h-100">
                    <div class="card-header">Camera 2</div>
                    <div class="card-body flex-grow-1 d-flex flex-column justify-content-center">
                        <h3 class="text-center">This is a blank page</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-6  camera_card text-center">
                <div class="card d-flex flex-column h-100">
                    <div class="card-header">Camera 3</div>
                    <div class="card-body flex-grow-1 d-flex flex-column justify-content-center">
                        <h3 class="text-center">This is a blank page</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-6 camera_card text-center">
                <div class="card  d-flex flex-column h-100">
                    <div class="card-header">Camera 4</div>
                    <div class="card-body flex-grow-1 d-flex flex-column justify-content-center">
                        <h3 class="text-center">This is a blank page</h3>
                    </div>
                </div>
            </div>
        </div>
    </>);
};

export default Dashboard;