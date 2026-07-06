import { useEffect } from "react";

function TrailerModal({ trailerKey, onClose }) {

    useEffect(() => {

        if (trailerKey) {

            window.open(
                `https://www.youtube.com/watch?v=${trailerKey}`,
                "_blank",
                "noopener,noreferrer"
            );

            onClose();
        }

    }, [trailerKey, onClose]);

    return null;

}

export default TrailerModal;