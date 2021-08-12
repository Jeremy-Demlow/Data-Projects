function job_state (task_id) {
    var taskID = task_id;
    // alert('ETL Job Submitted!');
    $.ajax({
        url: '/etl/'.concat(taskID),
        // url: '/etl/c346dcc0-8766-4bc9-a511-b05be596a278',
        // url: '/etl/c346dcc0-8766',
        type: 'get',
        success: function(data) {
            if (data.job_state == "SUCCESS") {
                // alert('Got a Success Statement');
                clearTimeout(job_state)
                document.getElementById("job_description").innerHTML = data.etl_info.description;
                document.getElementById("job_status").innerHTML = data.job_state;
                document.getElementById("job_responce").innerHTML = data.etl_info.responce;
                document.getElementById("progress_pic").innerHTML = "<img src='https://easy-migration-static.s3.amazonaws.com/static/loading/Done.png' style='width:100px;height:100px;'>";
            }
            else if (data.job_state == "FAILURE") {
                // alert('Got a Failure Statement');
                clearTimeout(job_state)
                document.getElementById("job_description").innerHTML = data.etl_info.description;
                document.getElementById("job_status").innerHTML = data.job_state;
                document.getElementById("job_responce").innerHTML = data.etl_info.responce;
                document.getElementById("progress_pic").innerHTML = "<img src='https://easy-migration-static.s3.amazonaws.com/static/loading/Fail.png' style='width:100px;height:100px;'>";
            }
            else if (data.job_state == "PENDING") {
                // alert('Got a Pending Statement');
                setTimeout(job_state, 1000, task_id);
                document.getElementById("job_description").innerHTML = data.etl_info.description;
                document.getElementById("job_status").innerHTML = data.job_state;
                document.getElementById("job_responce").innerHTML = data.etl_info.responce;
                document.getElementById("progress_pic").innerHTML = "<img src='https://media.giphy.com/media/sSgvbe1m3n93G/giphy.gif' style='width:100px;height:100px;'>";
            }
            else{
                // alert('Got an else statement');
                setTimeout(job_state, 1000, task_id);
                document.getElementById("job_description").innerHTML = data.etl_info.description;
                document.getElementById("job_status").innerHTML = data.job_state;
                document.getElementById("job_responce").innerHTML = data.etl_info.responce;
                document.getElementById("progress_pic").innerHTML = "<img src='https://media.giphy.com/media/sSgvbe1m3n93G/giphy.gif' style='width:100px;height:100px;'>";
            }
            
        },
        failure: function(data) {
            alert('Got an error');
        }
    })
    ;
}
