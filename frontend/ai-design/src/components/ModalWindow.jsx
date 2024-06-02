import React, { useState, useRef, useEffect } from 'react'
import style from './ModalWindow.module.css'

const ModalWindow = ({ message, handleModalClose }) => {

    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [selectedValue, setSelectedValue] = useState("Плакат А3");

    const toggleDropdown = () => {
        setDropdownOpen(!dropdownOpen);
    };

    const selectValue = (value) => {
        setSelectedValue(value);
        setDropdownOpen(false);
    };

    return (
        <div className={style.modal}>
            <div className={style.modalContent}>
                <div className={style.modalBody}>
                    <img src={message.imageUrl} alt="фото" />
                    <div className={style.artic}>
                        <svg className={style.close} width="19" height="19" viewBox="0 0 19 19" fill="none" xmlns="http://www.w3.org/2000/svg" onClick={handleModalClose}>
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M2.75723 0.83625C2.49954 0.59613 2.1587 0.465407 1.80653 0.471621C1.45436 0.477834 1.11835 0.6205 0.86929 0.869561C0.620229 1.11862 0.477563 1.45463 0.47135 1.8068C0.465136 2.15897 0.595859 2.49981 0.835979 2.7575L7.57848 9.5L0.835979 16.2425C0.702422 16.367 0.595299 16.517 0.521001 16.6838C0.446703 16.8505 0.406752 17.0305 0.403532 17.2131C0.400311 17.3956 0.433887 17.5769 0.502257 17.7461C0.570626 17.9154 0.672388 18.0692 0.801472 18.1983C0.930556 18.3273 1.08432 18.4291 1.25358 18.4975C1.42285 18.5658 1.60415 18.5994 1.78668 18.5962C1.9692 18.593 2.14921 18.553 2.31595 18.4787C2.4827 18.4044 2.63278 18.2973 2.75723 18.1637L9.49973 11.4213L16.2422 18.1637C16.3667 18.2973 16.5168 18.4044 16.6835 18.4787C16.8503 18.553 17.0303 18.593 17.2128 18.5962C17.3953 18.5994 17.5766 18.5658 17.7459 18.4975C17.9151 18.4291 18.0689 18.3273 18.198 18.1983C18.3271 18.0692 18.4288 17.9154 18.4972 17.7461C18.5656 17.5769 18.5991 17.3956 18.5959 17.2131C18.5927 17.0305 18.5528 16.8505 18.4785 16.6838C18.4042 16.517 18.297 16.367 18.1635 16.2425L11.421 9.5L18.1635 2.7575C18.4036 2.49981 18.5343 2.15897 18.5281 1.8068C18.5219 1.45463 18.3792 1.11862 18.1302 0.869561C17.8811 0.6205 17.5451 0.477834 17.1929 0.471621C16.8408 0.465407 16.4999 0.59613 16.2422 0.83625L9.49973 7.57875L2.75723 0.83625Z" fill="black" />
                        </svg>
                        <div className={style.icons}>
                            <button>
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M7 21L22 6L18 2L2 18L5 21H19M6 14L10 18" stroke="#333333" stroke-width="2" />
                                </svg>
                            </button>
                            <button>
                                T
                            </button>
                            <button>
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M13.5 6.5L17.5 10.5M4 20H8L18.5 9.5C18.7626 9.23735 18.971 8.92555 19.1131 8.58239C19.2553 8.23923 19.3284 7.87143 19.3284 7.5C19.3284 7.12856 19.2553 6.76077 19.1131 6.4176C18.971 6.07444 18.7626 5.76264 18.5 5.5C18.2374 5.23735 17.9256 5.02901 17.5824 4.88687C17.2392 4.74473 16.8714 4.67157 16.5 4.67157C16.1286 4.67157 15.7608 4.74473 15.4176 4.88687C15.0744 5.02901 14.7626 5.23735 14.5 5.5L4 16V20Z" stroke="#333333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                                </svg>
                            </button>
                            <button>
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M17.35 9.59736L15.22 11.7274L13.81 10.3074L6.1 18.0174L1.5 19.8774L0 18.3774L1.86 13.7774L9.57 6.06736L8.15 4.65736L10.28 2.52736L17.35 9.59736ZM14.76 0.87736C15.3225 0.315558 16.085 0 16.88 0C17.675 0 18.4375 0.315558 19 0.87736C19.5618 1.43986 19.8774 2.20236 19.8774 2.99736C19.8774 3.79236 19.5618 4.55486 19 5.11736L17.08 7.03736L12.84 2.79736L14.76 0.87736ZM3.56 14.9074L2.5 17.3774L4.97 16.3174L12.4 8.87736L11 7.47736L3.56 14.9074Z" fill="#333333" />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
                <div className={style.helps}>
                    <a className={style.dwnld} href={message.imageUrl} download>
                        <svg width="23" height="22" viewBox="0 0 23 22" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M16.067 8.02491L12.448 11.6439V0.0098877H10.25V11.6439L6.63106 8.02491L5.07681 9.57915L11.349 15.8514L17.6212 9.57915L16.067 8.02491ZM22.3397 19.7923V15.3962H20.1417V19.7923H2.55741V15.3962H0.359375V19.7923C0.359375 21.0062 1.34347 21.9903 2.55741 21.9903H20.1417C21.3556 21.9903 22.3397 21.0062 22.3397 19.7923Z" fill="#F2F2F2" />
                        </svg>
                        Скачать
                    </a>
                    <div className={style.dropdownButton} onClick={toggleDropdown}>
                        <p>{selectedValue}</p>
                        <svg width="12" height="6" viewBox="0 0 12 6" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M6.3293 5.87341L11.8643 0.734858C12.0455 0.566499 12.0452 0.293923 11.8634 0.125846C11.6815 -0.0421 11.3869 -0.041666 11.2055 0.126714L5.99998 4.9594L0.794435 0.12654C0.613029 -0.0418184 0.318632 -0.0422525 0.136757 0.125672C0.0455856 0.209928 -1.40011e-08 0.320308 -1.8826e-08 0.430688C-2.36385e-08 0.540786 0.0452804 0.650733 0.135819 0.734836L5.67068 5.87341C5.75782 5.9545 5.87642 6 5.99998 6C6.12354 6 6.24199 5.95437 6.3293 5.87341Z" fill="#222222" />
                        </svg>
                        {dropdownOpen && (
                            <div className={style.dropdown}>
                                <div className={style.dropdownItem} onClick={() => selectValue("Плакат A3")}>
                                    <p>Плакат A3</p>
                                    <p>297*420 мм</p>
                                </div>
                                <div className={style.dropdownItem} onClick={() => selectValue("Листовка А5")}>
                                    <p>Листовка А5</p>
                                    <p>148*210 мм</p>
                                </div>
                                <div className={style.dropdownItem} onClick={() => selectValue("Скринсейвер")}>
                                    <p>Скринсейвер</p>
                                    <p>1920*1080 px</p>
                                </div>
                                <div className={style.dropdownItem} onClick={() => selectValue("Баннер (интернет-портал)")}>
                                    <p>Баннер (интернет-портал)</p>
                                    <p>1200*593 px</p>
                                </div>
                                <div className={style.dropdownItem} onClick={() => selectValue("Баннер (новости)")}>
                                    <p>Баннер (новости)</p>
                                    <p>1200*520 px</p>
                                </div>
                                <div className={style.dropdownItem} onClick={() => selectValue("ТВ панель")}>
                                    <p>ТВ панель</p>
                                    <p>700*520 px</p>
                                </div>
                                <div className={style.dropdownItem} onClick={() => selectValue("Пост/новость")}>
                                    <p>Пост/новость</p>
                                    <p>1084*585 px</p>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ModalWindow