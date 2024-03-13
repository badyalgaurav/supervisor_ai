import React, { useRef, useState, useEffect } from 'react';
import Modal from 'react-modal';
import { apiWebSocketPath } from "../config";
Modal.setAppElement('#root');

const VideoModal = ({ isOpen, videoUrl, onRequestClose }) => {
    const [isVideoReady, setIsVideoReady] = useState(false);
    const [isVideoAvailable, setIsVideoAvailable] = useState(true);
    const videoRef = useRef(null);

    const f_path = `${apiWebSocketPath}/video/?video_path=${videoUrl}`;
    //const f_path = `${apiWebSocketPath}/video/?video_path=D:/var/www/output_camera_0/20240313/output_camera_0_20240313114115.mp4`;

    const handleVideoLoadedData = () => {
        // Video metadata has been loaded
        setIsVideoReady(true);
    };

    const handleVideoError = () => {
        // Video data is not available
        setIsVideoAvailable(false);
    };

    useEffect(() => {
        // Reset video availability on modal open
        setIsVideoAvailable(true);
    }, [isOpen]);

    return (
        <Modal
            isOpen={isOpen}
            onRequestClose={onRequestClose}
            style={{
                content: {
                    top: '50%',
                    left: '50%',
                    right: 'auto',
                    bottom: 'auto',
                    transform: 'translate(-50%, -50%)',
                    padding: 0
                },
            }}
            contentLabel="Video Modal"
        >
            <div className="modal-header">
                <h6 className="align-items-center">Video</h6>
                <button className="close-button" onClick={onRequestClose}>
                    X
                </button>
            </div>
            <div className="modal-content">
                {isVideoAvailable ? (
                    <video
                        ref={videoRef}
                        controls
                        width="100%"
                        height="100%"
                        onLoadedData={handleVideoLoadedData}
                        onError={handleVideoError}
                    >
                        <source src={f_path} type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                ) : (
                        <p className="error-text">Video data is not available. Please check after some time.</p>
                )}
            </div>
        </Modal>
    );
};

export default VideoModal;
