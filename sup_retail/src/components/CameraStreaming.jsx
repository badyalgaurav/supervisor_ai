import React, { useEffect, useState } from 'react';

const CameraStream = ({ cameraId }) => {
    const [imageSrc, setImageSrc] = useState('');

    useEffect(() => {
        const socket = new WebSocket(`ws://localhost:8000/ws/${cameraId}`);

        socket.binaryType = 'arraybuffer';

        socket.onmessage = function (event) {
            const imageUrl = URL.createObjectURL(new Blob([event.data], { type: 'image/jpeg' }));
            setImageSrc(imageUrl);
        };

        return () => {
            socket.close();
        };
    }, [cameraId]);

    return (<>
        <img src={imageSrc} alt={`Camera ${cameraId}`} style={{width:"100%"} } />
        <img src={imageSrc} alt={`Camera ${cameraId}`} />
        <img src={imageSrc} alt={`Camera ${cameraId}`} />    </>)
};

export default CameraStream;