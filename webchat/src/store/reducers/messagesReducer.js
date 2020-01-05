import { List } from 'immutable';
import { MESSAGE_SENDER, SESSION_NAME } from 'constants';

import {
    createQuickReply,
    createNewMessage,
    createLinkSnippet,
    createVideoSnippet,
    createImageSnippet,
    createControlSnippet,
    createComponentMessage,
    storeMessageTo,
    getLocalSession,
    storeParamsTo
} from './helper';

import {
  toggleFullScreen
} from '../actions/dispatcher';

import * as actionTypes from '../actions/actionTypes';

const WEBCHAT_TARGET_CONTENT = "webchat_target_content";

/**
 * @param {String} HTML representing a single element
 * @return {Element}
 */
function htmlToElement(html) {
  var template = document.createElement('template');

  html = html.trim(); // Never return a text node of whitespace as the result
  template.innerHTML = html;
  return template.content.firstChild;
}


export default function (storage) {

  const initialState = List([]);

  return function reducer(state = initialState, action) {
    const storeMessage = storeMessageTo(storage);
    const storeParams = storeParamsTo(storage);
    switch (action.type) {
      // Each change to the redux store's message list gets recorded to storage
      case actionTypes.ADD_NEW_USER_MESSAGE: {
        return storeMessage(state.push(createNewMessage(action.text, MESSAGE_SENDER.CLIENT)))
      }
      case actionTypes.ADD_NEW_RESPONSE_MESSAGE: {
        return storeMessage(state.push(createNewMessage(action.text, MESSAGE_SENDER.RESPONSE)));
      }
      case actionTypes.ADD_NEW_LINK_SNIPPET: {
        return storeMessage(state.push(createLinkSnippet(action.link, MESSAGE_SENDER.RESPONSE)));
      }
      case actionTypes.ADD_NEW_VIDEO_VIDREPLY: {
        return storeMessage(state.push(createVideoSnippet(action.video, MESSAGE_SENDER.RESPONSE)));
      }
      case actionTypes.ADD_NEW_IMAGE_IMGREPLY: {
        return storeMessage(state.push(createImageSnippet(action.image, MESSAGE_SENDER.RESPONSE)));
      }
      case actionTypes.ADD_NEW_CONTROL_CTLREPLY: {
        console.log("in reducer, message Reducer");
        // we might not want to storeMessage!
        //return storeMessage(state.push(createControlSnippet(action.control, MESSAGE_SENDER.RESPONSE)));
        const ctrl_snippet = createControlSnippet(action.control, MESSAGE_SENDER.RESPONSE);
        const background_url  = ctrl_snippet.get('background_url');
        if (background_url !== undefined) {
          const body = document.getElementsByTagName('body')[0];
          body.style.backgroundImage = ''.concat("url('", background_url, "')");
        }

        const background_color  = ctrl_snippet.get('background_color');
        if (background_color !== undefined) {
          const body = document.getElementsByTagName('body')[0];
          body.style.backgroundColor  =  background_color;
        }

        const fullscreen = ctrl_snippet.get('fullscreen');
        if (fullscreen !== undefined) {
          const wc = document.getElementsByClassName('widget-container')[0];
          const launcher = document.getElementsByClassName('launcher')[0];
            
          if (fullscreen) {
            wc.classList.add("full-screen");
            launcher.classList.add("full-screen");
            launcher.classList.add("hide");
          } else {
            wc.classList.remove("full-screen");
            launcher.classList.remove("full-screen");
            launcher.classList.remove("hide");
          }
        }

        const insert_html = ctrl_snippet.get('insert_html');
        if (insert_html !== undefined) {
          var target_div = document.getElementById(WEBCHAT_TARGET_CONTENT);
          if (target_div === undefined) {
            target_div = document.createElement("div"); 
            target_div.setAttribute("id", WEBCHAT_TARGET_CONTENT);
            document.body.appendChild(target_div)
          }
          var div_node = htmlToElement(insert_html);
          // remove all childrend node of target div
          while (target_div.firstChild) {
            target_div.firstChild.remove();
          }
          target_div.appendChild(div_node);
        }

        const append_html = ctrl_snippet.get('append_html');
        if (append_html !== undefined) {
          var target_div = document.getElementById(WEBCHAT_TARGET_CONTENT);
          if (target_div === undefined) {
            target_div = document.createElement("div"); 
            target_div.setAttribute("id", WEBCHAT_TARGET_CONTENT);
            document.body.appendChild(target_div)
          }
          var div_node = htmlToElement(append_html);
          // just append this child to the target div
          target_div.appendChild(div_node);
        }


        //toggleFullScreen();
        //state.update('fullScreenMode', fullScreenMode => !fullScreenMode)
        //return storeParams(state.update('fullScreenMode', fullScreenMode => !fullScreenMode));
        return state;
      }
      case actionTypes.ADD_QUICK_REPLY: {
        return storeMessage(state.push(createQuickReply(action.quickReply, MESSAGE_SENDER.RESPONSE)));
      }
      case actionTypes.ADD_COMPONENT_MESSAGE: {
        return storeMessage(state.push(createComponentMessage(action.component, action.props, action.showAvatar)));
      }
      case actionTypes.SET_QUICK_REPLY: {
        return storeMessage(state.setIn([action.id, 'chosenReply'], action.title));
      }
      case actionTypes.INSERT_NEW_USER_MESSAGE: {
        return storeMessage(state.insert(action.index, createNewMessage(action.text, MESSAGE_SENDER.CLIENT)));
      }
      case actionTypes.DROP_MESSAGES: {
        return storeMessage(initialState)
      }
      // Pull conversation from storage, parsing as immutable List
      case actionTypes.PULL_SESSION: {
        const localSession = getLocalSession(storage, SESSION_NAME);
        if (localSession) {
          return List(localSession.conversation);
        } else {
          return state
        }
      }
      default:
        return state;
    }
  }
}

