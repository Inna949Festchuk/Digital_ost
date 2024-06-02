import React, { useState } from 'react';
import style from "./ChatWindow.module.css"
import ModalWindow from './ModalWindow';

const ChatWindow = ({ messages }) => {
    const [modalOpen, setModalOpen] = useState(false);

    const handleModalOpen = () => {
        setModalOpen(true);
    };

    const handleModalClose = () => {
        setModalOpen(false);
    };

    return (
        <div className={style.main}>
            <div className={style.container}>
                {messages.map((message, index) => (
                    <div className={style.box} key={index}>
                        <img src={message.user ? "user-ai.png" : "chat-ai.png"} alt="" />
                        {message.user ? (
                            <div className={style.user}>
                                <p>{message.content}</p>
                            </div>
                        ) : (
                            <div className={style.answer}>
                                <img src={message.imageUrl} alt="Ответ от нейросети" />
                                <div>
                                    <a className={style.btn} href={message.imageUrl} download>Скачать</a>
                                    <button className={style.btnTwo} onClick={handleModalOpen}>Редактировать</button>
                                </div>
                            </div>
                        )}
                        {modalOpen && <ModalWindow message={message} handleModalClose={handleModalClose} />}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ChatWindow;