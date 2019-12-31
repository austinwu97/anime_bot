import React, { PureComponent } from 'react';
import { PROP_TYPES } from 'constants';

import './styles.scss';

class VidReply extends PureComponent {
  render() {
    console.log('in vidreply mode');
    const body = document.getElementsByTagName('body')[0];
    body.style.backgroundImage = 'url(https://assets.simpleviewinc.com/simpleview/image/upload/crm/palmsprings/JoshuaTreeNationalPark20-bc9b9a575056b36_bc9b9b3c-5056-b365-abf600cb2480c258.jpg)';
    return (
      <div className="video">
        <b className="video-title">
          { this.props.message.get('title') }
        </b>
        <div className="video-details">
          <iframe src={this.props.message.get('video')} className="videoFrame"></iframe>
        </div>
      </div>
    );
  }
}

VidReply.propTypes = {
  message: PROP_TYPES.VIDREPLY
};

export default VidReply;
