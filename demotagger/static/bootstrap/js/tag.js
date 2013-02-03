$(document).ready(function() {
  var tagging = false;
  var left = 0;
  var top = 0;
  var width, height;
  var currentTag;
  var video = $('#video');

  var tag_hash = {tag_frames: {}};

  $('body').mousedown(function(e) {
    var offset = video.offset();
    left = e.pageX-offset.left;
    top = e.pageY-offset.top;
    if (left < video.width() && top < video.height()) {
      tagging = true;
      $('#video_box').append('<div class="tag_box"></div>');
      currentTag = video.siblings('.tag_box').last();
      currentTag.css({'left': left, 'top': top});
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
        currentTag.remove();
      }
      var frame = tag_hash["tag_frames"][""+video[0].currentTime];
      if (frame == null) {
        frame = tag_hash["tag_frames"][""+video[0].currentTime] = {visual_tags:[]};
      }
      frame["visual_tags"].push({"visual_tag" : []});
      console.log(JSON.stringify(tag_hash));
    }
  })
  $('.comment').click(function(e) {
    console.log($(this).attr('data'));
    video[0].currentTime = $(this).attr('data');
  })
})