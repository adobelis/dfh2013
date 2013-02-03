$(document).ready(function() {
  var tagging = false;
  var left = 0;
  var top = 0;
  var width, height;
  var currentTag = $('#new_tag');
  var video = $('#video');

  var tag_hash = {tag_frames: {}};

  var tag_added = false;

  $('body').mousedown(function(e) {
    var offset = video.offset();
    left = e.pageX-offset.left;
    top = e.pageY-offset.top;
    if (left < video.width() && top < video.height()) {
      tagging = true;
      currentTag.css({'left': left, 'top': top, 'width':0, 'height':0});
      console.log(video[0].currentTime);
    }
  });
  $('body').mousemove(function(e) {
    if (tagging) {
      var offset = video.offset();
      var endX = e.pageX-offset.left;
      var endY = e.pageY-offset.top;
      if (endX < 0) {
        endX = 0;
      } else if (endX > video.width()) {
        endX = video.width()-2;
      }
      if (endY < 0) {
        endY = 0;
      } else if (endY > video.height()) {
        endY = video.height()-2;
      }
      width = endX-left;
      height = endY-top;
      if (width < 0) {
        currentTag.css({'left': left+width, 'width':-width});
      } else {
        currentTag.css({'left': left, 'width':width});
      }
      if (height < 0) {
        currentTag.css({'top': top+height, 'height':-height});
      } else {
        currentTag.css({'top': top, 'height':height});
      }
    }
  })
  $('body').mouseup(function(e) {
    if (tagging) {
      tagging = false;
      var offset = video.offset();
      var endX = e.pageX-offset.left;
      var endY = e.pageY-offset.top;
      if (endX == left && endY == top) {
        //currentTag.remove();
      } else {
        tag_added = true;
        if (width < 0) {
          currentTag.css({'left': left+width, 'width':-width});
        } else {
          currentTag.css({'left': left, 'width':width});
        }
        if (height < 0) {
          currentTag.css({'top': top+height, 'height':-height});
        } else {
          currentTag.css({'top': top, 'height':height});
        }
      }
    }
  })
  $('.comment').click(function(e) {
    console.log($(this).attr('data'));
    video[0].currentTime = $(this).attr('data');
  })
  $('#add_comment').click(function(e) {
    var data = {workspace_id: workspace_id, frame_time: video[0].currentTime, commenter_id: user_id,
          left: parseInt(currentTag.css('left')),
          top: parseInt(currentTag.css('top')),
          width: currentTag.width(),
          height: currentTag.height()};
    console.log(data);
    $.post('/media_wkf/add_comment/',
        JSON.stringify(data),
        function(data) {
          currentTag.css({'width':0, 'height':0});
          $('#video_box').append('<div class="tag_box"></div>');
          video.siblings('.tag_box').last().css({'left': currentTag.css('left'), 'top': currentTag.css('top'), 'width': currentTag.width(), 'height': currentTag.height()});
        }
      );
  })
})