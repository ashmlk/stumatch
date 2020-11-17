import React from 'react';

const Sidepanel = (props) => (

    <div id="sidepanel">
        <div id="contacts">
            <div id="search">
                <label htmlFor=""><i className="fa fa-search" aria-hidden="true"></i></label>
                <input type="text" placeholder="Search contacts..." />
            </div>
            <ul>
                <li className="contact">
                    <div className="wrap">
                        <span className="contact-status online"></span>
                        <img src="http://emilcarlsson.se/assets/louislitt.png" alt="" />
                        <div className="meta">
                            <p className="name">Louis Litt</p>
                            <p className="preview">You just got LITT up, Mike.</p>
                        </div>
                    </div>
                </li>
                <li className="contact active">
                    <div className="wrap">
                        <span className="contact-status busy"></span>
                        <img src="http://emilcarlsson.se/assets/harveyspecter.png" alt="" />
                        <div className="meta">
                            <p className="name">Harvey Specter</p>
                            <p className="preview">Wrong. You take the gun, or you pull out a bigger one. Or, you call
                                their bluff. Or, you do any one of a hundred and htmlForty six other things.</p>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </div>
)

export default Sidepanel;