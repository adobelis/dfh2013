

$(document).ready(function() {
  var tagging = false;
  var left = 0;
  var top = 0;
  var width, height;
  var tag_hash = {tag_frames: {}};
  var tag_added = false;
  var context = -1;
  var currentTag = $('#new_tag');
  var video = $('#video');

  $('.comment-bar').hide();
  $('body').mousedown(function(e) {
    var offset = video.offset();
    left = e.pageX-offset.left;
    top = e.pageY-offset.top;
    if (left < video.width() && top < video.height()-30) {
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
  $('#add_comment').click(function(e) {
    console.log("hello");
    var data = {workspace_id: workspace_id, media_item_id: media_item_id, video_frame_ctxt_id: context, frame_time: video[0].currentTime, commenter_id: user_id,
          left: parseInt(currentTag.css('left')),
          top: parseInt(currentTag.css('top')),
          width: currentTag.width(),
          height: currentTag.height(),
          comment_text: $('#new_comment').val()};
          console.log(data);
    $.post('/media_wkf/add_comment/',
        {"data": JSON.stringify(data)},
        function(data) {
          var ctxt_id = data['video_frame_ctxt_id'];
          var matching_frame = $(".frame_context[data-id="+ctxt_id+"]");
          if (matching_frame.length == 0) {
            matching_frame = $("<div class='frame_context' data-id="+ctxt_id+" />");
            $('#comment_section').append(matching_frame);
          }
          var tag_id = data['tag_id'];
          var tag = $("<div class='visual_tag' data-id="+tag_id+" />");
          matching_frame.append(tag);
          
          //$('.tag_box').last().attr('data-frame', ctxt_id);
          var new_comment = $('#new_comment');
          var comment = $("<div class='comment' data-frame="+video[0].currentTime+"><div class='text'>"+new_comment.val()+"</div></div>");
          tag.append(comment).slideDown();
          comment.click(function(e) {
            video[0].currentTime = $(this).attr('data-frame');
            video.trigger("timeupdate");
            $(".tag_box[data-id="+$(this).parent().attr('data-id')+"]").show();
          })
          comment.mouseenter(function(e) {
            $(this).addClass('hover');
            $(".tag_box[data-id="+$(this).parent().attr('data-id')+"]").addClass('hover');
          })
          comment.mouseleave(function(e) {
            $(this).removeClass('hover');
            $(".tag_box[data-id="+$(this).parent().attr('data-id')+"]").removeClass('hover');
          })
          new_comment.val('');
          var tag_box = $("<div class='tag_box' data-frame="+data['video_frame_ctxt_id']+" data-id="+tag_id+"/>");
          tag_box.mouseenter(function(e) {
            $(this).addClass('hover');
            $(".visual_tag[data-id="+$(this).attr('data-id')+"] .comment").addClass('hover');
          })
          tag_box.mouseleave(function(e) {
            $(this).removeClass('hover');
            $(".visual_tag[data-id="+$(this).attr('data-id')+"] .comment").removeClass('hover');
          })
          $('#video_box').append(tag_box);
          video.siblings('.tag_box').last().css({'left': currentTag.css('left'), 'top': currentTag.css('top'), 'width': currentTag.width(), 'height': currentTag.height()});
          currentTag.css({'width':0, 'height':0, 'left':-8});
          console.log('hello');
        }
      );
  })
  video[0].addEventListener("timeupdate", function () {
      //  Current time  
      var vTime = video[0].currentTime;
      context = null;
      var mindiff = 1;
      for (var i in frame_times) {
        var frame = frame_times[i];
        var diff = Math.abs(frame.time-video[0].currentTime);
        if (diff<mindiff) {
          mindiff = diff;
          context = frame.id;
        }
      }
      console.log(context);
      $('.tag_box').each(function() {
        if ($(this).attr('data-frame') == context) {
          $(this).show();
        } else {
          $(this).hide();
        }
      })
  }, false);

  $('.comment').click(function(e) {
    video[0].currentTime = $(this).attr('data-frame');
  })

  $('.comment').mouseenter(function(e) {
    alert('hello');
    $(".tag_box[data-id="+$(this).parent().attr('data-id')+"]").addClass('hover');
  })
})