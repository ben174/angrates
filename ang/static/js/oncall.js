jQuery(document).ready(function() {
  var isMouseDown = false; 
  jQuery(".calendar td").mousedown(function() { 
    isMouseDown = true; 
    jQuery(this).toggleClass("selected");
    isSelected = $(this).hasClass("selected");
    return false; // prevent text selection
  })
  .mouseover(function() { 
    if(isMouseDown) { 
      $(this).toggleClass("selected", isSelected); 
    }
  });    
  $(document).mouseup(function () {
      isMouseDown = false;
      updateHiddenField();
  });
});


function updateHiddenField() { 
  val = ""; 
  jQuery(".selected").each(function() { 
    val += jQuery(this).attr("date").split("/").join("-")+","; 
  }); 
  console.log(val);
  if(val=="") { 
    jQuery("#create-assignment-btn").attr('disabled', 'disabled');
  } else { 
    jQuery("#create-assignment-btn").removeAttr('disabled');
  }

  jQuery("#dates").val(val);
}

function getShifts(groupID) { 
  jQuery('#shift').empty(); 
  jQuery.getJSON("/oncall/json/shifts/" + groupID, function(data) { 
    jQuery.each(data, function(index, val) { 
      key = val.pk; 
      text = val.fields.start_time + ' - ' + val.fields.stop_time; 
      jQuery('#shift')
         .append(jQuery("<option></option>")
         .attr("value",key)
         .text(text)); 
    }); 
    jQuery('.shift-assignment').toggle(data.length>1);
  }); 
}
