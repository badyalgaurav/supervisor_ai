import React, { useState, useEffect } from 'react';

const Login= () => {
    return (<>
        <div class="container-fluid pt-4 px-4">
            <p>welcome to Setting Page page</p>
            <p>Number of camers to setup</p>
            <input type="text" placeholder="number of cameras"></input>
            <p>Camera company</p>
            <select><option>Hikvision</option></select>

            <p>Next, Camera 1</p>
            <select><option>IP address</option></select>
            <select><option>Port address</option></select>
            <button>Next camera setup</button>
            <button>Final setup</button>
        </div>
    </>);
};

export default Login;