import React, { useState } from 'react';
import DataTable from 'react-data-table-component';
import { useNavigate } from 'react-router-dom';
import VideoModal from '../../components/VideoModal'; // Import the modal component

//import 'react-data-table-component/styles.css';
const AlertEventsReport = () => {
    const navigate = useNavigate();


    const data = [
        { id: 1, name: 'John Doe', age: 30, city: 'New York' },
        { id: 2, name: 'Jane Smith', age: 25, city: 'Los Angeles' },
        // Add more data rows here
    ];

    const columns = [
        {
            name: 'ID',
            selector: 'id',
        },
        {
            name: 'Name',
            selector: 'name',
        },
        {
            name: 'Age',
            selector: 'age',
        },
        {
            name: 'City',
            selector: 'city',
        },
        {
            name: 'Video',
            cell: (row) => (
                <button onClick={() => openModal(row.cityl)}>Play Video</button>
            ),
        },
    ];

    // Function to open the modal
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [videoUrl, setVideoUrl] = useState('');

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
        alert(page)
        // Use the history object to navigate to the desired page
        const params = {
            contentId: "test"
        };
        navigate('/', { state: params });
    };
    return (<>
        <div class="bg-secondary rounded align-items-center mx-0" id="alertEventContainer">
            <div><button onClick={() => { handleTaskClick("test") }}>Go back</button></div>
            <div class="card">
            <DataTable
                title="My Data Table"
                columns={columns}
                data={data}
                selectableRows
                pagination
                />
                <VideoModal isOpen={modalIsOpen} videoUrl={videoUrl} onRequestClose={closeModal} />
        </div>
        </div>
    </>);
};

export default AlertEventsReport;