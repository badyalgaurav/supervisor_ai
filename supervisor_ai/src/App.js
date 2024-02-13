import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";

import Layout from './pages/master/_layout';
import Dashboard from './pages/dashboard/Dashboard';
import FabricOrg from './pages/rnd/fabricOrg';
import AlertEventsReport from './pages/reports/AlertEventsReport';
import Login from './pages/login/Login';

function Root() {
    const navigate = useNavigate();
    //const [changeState, setChangeState] = useState();

    //useEffect(() => {
    //    if (!sessionStorage.getItem("userId")) {
    //        navigate('/login', { replace: true });
    //    }

    //}, []);
  


    return (
        <div>
            <Routes>
                <Route path="/Login" element={<Login />} />
                <Route path="/FabricOrg" element={<FabricOrg />} />
                <Route path="/" element={<Layout />}>
                    <Route path="/" element={<Dashboard />} />
                    
                    <Route path="/AlertEventsReport" element={<AlertEventsReport />} />
                </Route>
            </Routes>
        </div>);

};

const App = () => {
    return (
        <BrowserRouter>
            <Root />
        </BrowserRouter>
    );
};

export default App;
