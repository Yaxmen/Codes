(function executeRule (current,previous /*null when async*/ ) {

    // scoped GlideSystem logging methods
    gs.info("this is an info message from the NeedIt app.");
    gs.warn("this is a warning mesage from the NeedIt app.");
    gs.error("this is an error message from the NeedItapp.");
    gs.debug("this is a debug message from the NeedItApp.");

})(current, previous);