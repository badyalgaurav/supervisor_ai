import React, { useState, useEffect } from 'react';
//import DataTable, { createTheme } from 'react-data-table-component';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import VideoModal from '../../components/VideoModal'; // Import the modal component
// date picker reference : https://reactdatepicker.com/
import DatePicker from "react-datepicker";
import moment from 'moment';
import "react-datepicker/dist/react-datepicker.css";
import { apiSAIFrameworkAPIPath } from "../../config"
import DataTableComponent from "../../components/dataTable/DataTableComponent"
import { useLocation } from 'react-router-dom';


const AlertEventsReport = () => {
    const { state } = useLocation();
    const { cameraId } = state; // Read values passed on state

    const navigate = useNavigate();
    // Function to open the modal
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [videoUrl, setVideoUrl] = useState('');
    const initColumns = [
        {
            name: 'cameraId',
            selector: 'cameraId',
        },
        {
            name: 'startTime',
            selector: 'startTime',
        },
        {
            name: 'endTime',
            selector: 'endTime',
        },
        {
            name: 'Video',
            cell: (row) => (


                <button className="btn btn-primary" onClick={() => openModal(row.videoPath)}><i className="fa fa-play"></i></button>
            ),
        },
    ];
    const [data, setData] = useState([]);
    const [columns, setColumns] = useState(initColumns);

    const [dateRange, setDateRange] = useState([new Date(), new Date()]);
    const [startDate, endDate] = dateRange;

    // Function to handle date range selection

    const handleGetData = () => {
        const apiUrl = `${apiSAIFrameworkAPIPath}/mongo_op/get_alert_details/`; // Replace with your API endpoint URL
        const requestData = {
            "camera_id": parseInt(cameraId),
            "start_date": moment(startDate).format('YYYY-MM-DD'),
            "end_date": moment(endDate).format('YYYY-MM-DD'),
        };

        axios.get(apiUrl, { params: requestData })
            .then((response) => {
                const responseData = response.data.data;
                setData(responseData);
            })
            .catch((error) => {
                // Handle any errors that occurred during the request
                console.error('Error:', error);
            });
    }

    useEffect(() => {
        handleGetData()
    }, [cameraId]);




    const openModal = (url) => {
        debugger;
        setVideoUrl(url);
        setModalIsOpen(true);
    };

    const closeModal = () => {
        setModalIsOpen(false);
        setVideoUrl('');
    };
    const handleTaskClick = (page) => {

        // Use the history object to navigate to the desired page
        const params = {
            contentId: "test"
        };
        navigate('/', { state: params });
    };



    return (<>
        <div class="container-fluid pt-4 px-4">


            <div class="d-flex align-items-center justify-content-between mb-4">
                <h6 class="mb-0">Alerts</h6>
                <div>

                    <div style={{ display: 'flex', alignItems: 'center' }}>
                    
                        <DatePicker
                            selectsRange={true}
                            startDate={startDate}
                            endDate={endDate}
                            onChange={(update) => {
                                setDateRange(update);
                            }}
                            
                            dateFormat="yyyy/MM/dd"
                                className="custom-datepicker-input"
                            />
                      
                        <button type="button" class="btn btn-outline-info m-2" onClick={() => { handleGetData("test") }}><i class="fa fa-search me-2"></i>Search</button>
                        <button type="button" class="btn btn-outline-success m-2" onClick={() => { handleTaskClick("test") }}><i class="fa fa-home me-2"></i>Dashboard</button>
                    </div>
                </div>

            </div>

            <div class="card">
                <DataTableComponent columns={columns} data={data} />
                <VideoModal isOpen={modalIsOpen} videoUrl={videoUrl} onRequestClose={closeModal} />
            </div>
        </div>
    </>);
};

export default AlertEventsReport;