import React from 'react';
import Sidepanel from './Sidepanel/Sidepanel';
import WebSocketInstance from '../websocket';

class Chat extends React.Component {

    constructor(props) {
        super(props)
        this.state = {}
        this.waitForSocketConnection(() => {
            WebSocketInstance.addCallbacks(
                this.setMessages.bind(this), 
                this.addMessage.bind(this));
            WebSocketInstance.fetchMessages(this.props.currentUser);
        });
    }


    waitForSocketConnection(callback) {
        const component = this;
        setTimeout(
            function() {
                if (WebSocketInstance.state() === 1) {
                    console.log('connection is secured');
                    callback();
                    return;
                }
                else {
                    console.log('waiting for connection');
                    component.waitForSocketConnection(callback);
                }

        }, 100);
    }

    addMessage(message) {
        this.setState({
            message: [...this.state.messages, message]
        });
    }

    setMessages(messages) {
        this.setState({  
            messages:messages.reverse()     
        });
    }

    sendMessageHandler = e => {
        e.preventDefault();
        const messageObject = {
            from: 'admin',
            content: this.state.message
        }
        WebSocketInstance.newChatMessage(messageObject);
        this.setState({
            message:''
        })
    }

    messageChangeHandler = event => {
        this.setState({
            message: event.target.value
        })
    }

    renderMessages = (messages) => {
        const currentUser = 'admin';
        return messages.map(message => {
            <li 
                key={message.id}
                className={message.author === currentUser ? 'sent' : 'replies'}>
                <img src={message.img}/>
                <p>
                    {message.content}
                    <br />
                    <small>
                        {Math.round((new Date().getTime() - new Date(message.timestamp).getTime())/60000)}
                    </small>
                </p>

            </li>
        })
    }

    render() {
        const messages = this.state.messages;
        return (
            <div id="frame">
                <Sidepanel />
                <div className="content">
                    <div className="contact-profile">
                        <img alt="" />
                        <p className="font-weight-bold text-dark">@username</p>
                        <div className="social-media">
                            <i className="fa fa-facebook" aria-hidden="true"></i>
                            <i className="fa fa-twitter" aria-hidden="true"></i>
                            <i className="fa fa-instagram" aria-hidden="true"></i>
                        </div>
                    </div>
                    <div className="messages">
                        <ul id="chat-log">
                            {
                                messages &&
                                this.renderMessages(messages)
                            }
                        </ul>
                    </div>
                    <div className="message-input border-left">
                        <form onSubmit={this.sendMessageHandler}>
                            <div className="wrap">
                                <input 
                                    onChange={this.messageChangeHandler}
                                    value={this.state.message}
                                    type="text" 
                                    className='m-1' 
                                    id="chat-message-input" 
                                    placeholder="Send a message"/>
                                <button 
                                    style={{borderRadius:"18px"}}
                                    className="m-1 submit btn btn-primary btn-md" 
                                    id="chat-message-submit"
                                    >Send</button>
                            </div>
                        </form>                 
                    </div>
                </div>
            </div>
        )
    }
}

export default Chat;