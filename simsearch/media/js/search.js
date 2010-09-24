/*
 *
 *  search.py
 *  simsearch
 * 
 *  Created by Lars Yencken on 31-08-2010.
 *  Copyright 2010 Lars Yencken. All rights reserved.
 *
 */

/*
 * GLOBALS
 */

// The fraction of the screen's width or height to use for the lookup pane.
var g_useFraction = 0.8;

// A history of data, so that we can provide backwards and forwards
// navigation.
var g_historyStore = new Array();
var currentIndex = null;

// The current "mode" of the interface.
var g_currentState = 'seeding';

// Extra state about what's currently being displayed. Only updated by objects
// that need it on draw() and clean() operations, primarily to avoid excessive
// redraws.
var g_currentObjects = {}
var g_windowDirty = false;

/*
 * drawError()
 *      Draws an error message to the screen.
 */
function drawError(messageEn, messageJp, timeout) {
    // Render it, but still hidden, so we can check its size.
    g_currentObjects['errorMessage'] = [messageEn, messageJp, timeout]
    setOpacity('errorMessage', 0.01);
    showElement('errorMessage');

    // Delete any previous messages.
    var parentNode = $('errorMessage')
    while (parentNode.childNodes.length > 0) {
        c = parentNode.childNodes[0];
        parentNode.removeChild(c);
        delete c;
    }

    // Add our messages.
    parentNode.appendChild(document.createTextNode(messageEn))
    parentNode.appendChild(document.createElement('br'));
    parentNode.appendChild(document.createTextNode(messageJp))

    var errorSize = getElementDimensions('errorMessage');
    var seedInputSize = getSeedingInputSize();
    var seedInputLoc = getElementPosition(document['seedForm'].seedKanji);
    var windowSize = getWindowSize();

    var errorLoc = new Coordinates();
    errorLoc.x = Math.round(seedInputLoc.x + seedInputSize.w/2 - errorSize.w/2);
    errorLoc.y = seedInputLoc.y + seedInputSize.h + 50;

    setElementPosition('errorMessage', errorLoc);

    appear('errorMessage');
    drawSearch(false);
    if (timeout > 0) {
        callLater(timeout, function(){
            fade('errorMessage');
            delete g_currentObjects["errorMessage"];
        });
    }
}

/*
 * clearError()
 *      Hides any error messages that are shown.
 */
function clearError() {
    hideElement('errorMessage');
}

/*
 * getSeedingInputSize()
 *      Returns the size of the combined input element.
 */
function getSeedingInputSize() {
    setOpacity('seedLookup', 0.01);
    showElement('seedLookup');
    // Get the elements.
    var magnifier = document['magnifier'];
    var seedKanjiInput = document['seedForm'].seedKanji

    // Determine their sizes.
    var inputSize = getElementDimensions(seedKanjiInput);
    var magSize = getElementDimensions(magnifier);

    // Calculate the combined size.
    var combinedSize = new Dimensions();
    var padding = 5;
    combinedSize.w = inputSize.w + padding + magSize.w;
    combinedSize.h = magSize.h;

    return combinedSize;
}

/*
 * drawSeedingInput()
 *      Draw the initial input dialog.
 */
function drawSeedingInput(useAppear) {
    drawSearch(useAppear);
    if ("errorMessage" in g_currentObjects) {
        var em = g_currentObjects["errorMessage"];
        drawError(em[0], em[1], em[2]);
    }
}

function drawSearch(useAppear) {
    if (useAppear == null) {
        useAppear = true;
    }

    // Calculate the coordinates.
    var windowSize = getWindowSize();
    var inputLoc = new Coordinates();
    var combinedSize = getSeedingInputSize();
    inputLoc.x = Math.round(0.5*(windowSize.w - combinedSize.w));
    inputLoc.y = Math.round(0.5*(windowSize.h - combinedSize.h));

    // Center and make the input appear.
    setElementPosition('seedLookup', inputLoc);
    if (useAppear) {
        appear('seedLookup');
        callLater(1, function() { document['seedForm'].seedKanji.focus();});
    } else {
        setOpacity('seedLookup', 1.0);
        document['seedForm'].seedKanji.focus();
    }
}

/*
 * clearSeedingInput()
 *      Clear the initial seeding input dialog.
 */
function clearSeedingInput() {
    hideElement('seedLookup');
    hideElement('errorMessage');
    return;
}

/*
 * switchState()
 *      Switches from one UI state to another.
 */
function switchState(newState, stateArg) {
    g_clearState[g_currentState]();
    g_currentState = newState;
    g_initState[newState](stateArg);
}

/*
 * submitSeed()
 */
function submitSeed() {
    var value = document['seedForm'].seedKanji.value;

    var messageEn = "Please enter a single kanji only.";
    var messageJp = '一つの漢字を入力してください。';

    if (value.length != 1) {
        drawError(messageEn, messageJp, 6);
    } else {
        // Check that the input is a kanji.
        logDebug("Ok value: " + value);
        var valueOrd = ord(value);
        if (valueOrd < 12353 || valueOrd > 40869) {
            drawError(messageEn, messageJp, 6);
        } else {
            // Valid!
            switchState("lookup", value);
        }
    }
    return false;
}

/*
 * initLookup()
 *      Loads the kanji which are similar to the current pivot.
 */
function initLookup(pivotKanjiVal) {
    if (currentIndex != null) {
        var previousKanji = g_historyStore[currentIndex].pivotKanji;
        var newDoc = loadJSONDoc(g_pivotPath + pivotKanjiVal + "/", {});
    } else {
        var newDoc = loadJSONDoc(g_pivotPath + pivotKanjiVal + "/", {});
    }

    var success = function(obj) {
        // Store current values, and redraw the screen.
        // Determine whether truncation is needed.
        if (currentIndex == null) {
            // First time.
            currentIndex = 0;
        } else if (g_historyStore.length > currentIndex + 1) {
            // Truncation needed!
            currentIndex++;
            g_historyStore.length = currentIndex;
        } else {
            currentIndex++;
        }
        g_historyStore[currentIndex] = obj;

        drawBorder();
        drawLookup();
    }

    var failure = function(err) {
        logDebug("Couldn't load data: " + err);
        switchState('seeding', null);
        drawError('No data found for the kanji ' + pivotKanjiVal + '.', '',
                6);
    }

    newDoc.addCallbacks(success, failure);
};

/*
 * fullRedraw()
 *      Redraws the whole screen, using the existing kanji.
 */
function fullRedraw() {
    g_windowDirty = true;
    g_drawState[g_currentState]();
    g_windowDirty = false;
};

// Redraw the window if it is resized.
window.onresize = fullRedraw;

/*
 * getLookupPlane()
 *      Fetches the full plane size of the area.
 */
function getLookupPlane() {
    var windowSize = getWindowSize();
    var lookupPlane = {};
    lookupPlane.w = g_useFraction*windowSize.w;
    lookupPlane.h = g_useFraction*windowSize.h;

    // Make it square.
    if (lookupPlane.w < lookupPlane.h) {
        lookupPlane.h = lookupPlane.w;
    } else {
        lookupPlane.w = lookupPlane.h;
    }

    // Make it centered.
    lookupPlane.left = Math.round((windowSize.w - lookupPlane.w)/2);
    lookupPlane.right = lookupPlane.left + lookupPlane.w;
    lookupPlane.top = Math.round((windowSize.h - lookupPlane.h)/2);
    lookupPlane.bottom = lookupPlane.top + lookupPlane.h;

    lookupPlane.center = new Coordinates(
            lookupPlane.left + lookupPlane.w/2,
            lookupPlane.top + lookupPlane.h/2
        );

    return lookupPlane;
};

/*
 * drawBorder()
 *      Draws a border around the kanji area.
 */
function drawBorder() {
    if (g_currentObjects['border'] && !g_windowDirty) {
        return;
    }
    logDebug('Drawing border');
    // Work out the dimensions.
    var lookupPlane = getLookupPlane();

    // Generate the new border.
    var styleString = "position:absolute; ";
    styleString += 'left: ' + lookupPlane.left + 'px; '
    styleString += 'right: ' + lookupPlane.right + 'px; '
    styleString += 'top: ' + lookupPlane.top + 'px; '
    styleString += 'bottom: ' + lookupPlane.bottom + 'px; '
    styleString += 'width: ' + lookupPlane.w + 'px; '
    styleString += 'height: ' + lookupPlane.h + 'px; '
    var newBorder = DIV({style: styleString, id:"lookupBorder"}, "");

    // Swap it for the old border.
    swapDOM("lookupBorder", newBorder);

    setOpacity("lookupBorder", 1.0);
    g_currentObjects['border'] = true;
};

/* 
 * clearBorder()
 *      Clears the border around the kanji area.
 */
function clearBorder() {
    logDebug('Clearing border');
    setOpacity('lookupBorder', 0.0);
    g_currentObjects['border'] = false;
}

/*
 * getControlPlane()
 *      Determine the placement of the control plane.
 */
function getControlPlane() {
    var windowSize = getWindowSize();
    var lookupPlane = getLookupPlane();

    var controlPlane = {};
    controlPlane.top = lookupPlane.bottom;
    controlPlane.bottom = windowSize.h;
    controlPlane.left = lookupPlane.left;
    controlPlane.right = lookupPlane.right;
    controlPlane.w = controlPlane.right - controlPlane.left;
    controlPlane.h = controlPlane.bottom - controlPlane.top;

    controlPlane.center = new Coordinates(
            controlPlane.left + controlPlane.w/2,
            controlPlane.top + controlPlane.h/2
        );

    return controlPlane;
}

/* 
 * clearControls()
 *      Clears the controls from the display.
 */
function clearControls() {
    hideElement("backControl");
    hideElement("forwardControl");
    hideElement("resetControl");
    return;
}

/*
 * drawControls()
 *      Repositions the back and forward links dynamically. 
 */
function drawControls() {
    // Fetch location and size information needed for calculations.
    var controlPlane = getControlPlane();

    //var backSize = elementDimensions(document["backControl"]);
    //var forwardSize = elementDimensions(document["forwardControl"]);
    var backSize = new Dimensions(30, 35);
    var forwardSize = new Dimensions(30, 35);
    var resetSize = new Dimensions(35, 35);

    var top = Math.round(controlPlane.top + controlPlane.h/2 - 35/2);
    var backPos = new Coordinates(controlPlane.left, top);

    var forwardPos = new Coordinates(controlPlane.right - backSize.w, top);

    var resetPos = new Coordinates(
            Math.round(controlPlane.left + controlPlane.w/2 - resetSize.w/2),
            top
        );

    setElementPosition("backControl", backPos);
    setElementPosition("forwardControl", forwardPos);
    setElementPosition("resetControl", resetPos);

    appear("resetControl");

    if (hasHistory()) {
        appear("backControl");
    } else {
        hideElement("backControl");
    }

    if (hasFuture()) {
        appear("forwardControl");
    } else {
        hideElement("forwardControl");
    }

    g_currentObjects['controls'] = true;

    return;
};

/*
 * clearKanji()
 */
function clearKanji() {
    // Hide the existing elements.
    var existingElements = getElementsByTagAndClassName("div", "similarKanji");
    for (var i = 0; i < existingElements.length; i++) {
        removeElement(existingElements[i]);
    }
    setOpacity('pivotKanji', 0.0);

    g_currentObjects['controls'] = false;
}

/*
 * clearLookup()
 *      Clears any kanji currently displayed.
 */
function clearLookup() {
    logDebug('Clearing lookup');

    clearKanji();
    clearControls();
    clearBorder();

    // Clear the history too.
    g_historyStore.length = 0;
    currentIndex = null;
    return;
}

/*
 * drawLookup()
 *      Draws the existing dataset to the screen.
 */
function drawLookup() {
    drawBorder();
    drawControls();
    drawKanji();
}

/*
 * drawKanji()
 *      Draws the lookup kanji to the window.
 */
function drawKanji() {
    logDebug("Drawing kanji");
    clearKanji();

    // Draw the new pivot.
    var lookupPlane = getLookupPlane();
    var pivotLoc = toCornerLoc(lookupPlane.center);
    var pivotKanji = g_historyStore[currentIndex].pivot_kanji;
    var path = ""
    for (var i = 0; i < g_historyStore.length; i++) {
        path += g_historyStore[i]['pivot_kanji']
    }

    newPivot = DIV(
            {
                id: "pivotKanji",
                style: locToStyle(pivotLoc)
            }, 
            A(
                {href: g_translatePath + pivotKanji + "/?path=" + path},
                pivotKanji
            )
        );
    swapDOM("pivotKanji", newPivot);

    var tier1 = g_historyStore[currentIndex].tier1;
    var tier2 = g_historyStore[currentIndex].tier2;
    var tier3 = g_historyStore[currentIndex].tier3;

    drawTier(tier1, 1);
    drawTier(tier2, 2);
    drawTier(tier3, 3);

    callLater(0.1, function() {
        showClass('tier1Kanji');
        callLater(0.1, function() {
            showClass('tier2Kanji');
            callLater(0.1, function() {
                showClass('tier3Kanji');
            });
        });
    });

    return;
}

/*
 * locAdd(locA, locB)
 *      Addition of coordinates, returns the result.
 */
function locAdd(locA, locB) {
    return new Coordinates(locA.x + locB.x, locA.y + locB.y);
}

/*
 * drawTier(kanjiArray, tierNumber)
 *      Draws the given numbered tier (can be 1, 2 or 3), and spaces out the
 *      given kanji evenly upon that tier.
 */
function drawTier(kanjiArray, tierNumber) {
    logDebug("Drawing tier " + tierNumber);
    var lookupPlane = getLookupPlane();

    var center = lookupPlane.center;
    var angleFraction = 2*Math.PI/kanjiArray.length; 
    var radius = tierNumber*lookupPlane.w/8;
    var initialFraction = Math.random()*angleFraction;

    // Generate new elements for the kanji.
    var newElements = new Array();
    for (var i = 0; i < kanjiArray.length; i++) {
        var kanji = kanjiArray[i];
        var loadCommand = "initLookup('" + kanji + "')";

        var kanjiAngle = initialFraction + i*angleFraction;
        var loc = new Coordinates(
                radius*Math.cos(kanjiAngle),
                radius*Math.sin(kanjiAngle)
            )
        loc = locAdd(loc, lookupPlane.center);
        loc = toCornerLoc(loc);
        newElements[i] = DIV(
                {
                    class: "tier" + tierNumber + "Kanji similarKanji", 
                    style: "opacity:0.0; " + locToStyle(loc),
                },
                A(
                    {
                        href: "javascript:;",
                        onclick: loadCommand
                    },
                    kanji
                )
            );
    }

    var body = document.getElementsByTagName("body")[0];
    appendChildNodes(body, newElements);

    return;
};

/*
 * showClass()
 *      Make all the DIV elements of this class appear.
 */
function showClass(className) {
    newElements = getElementsByTagAndClassName("div", className);
    for (var i = 0; i < newElements.length; i++) {
        setOpacity(newElements[i], 1.0);
    }
}

/*
 * getWindowSize()
 *      Returns the size in pixels of the browser window as a (width, height)
 *      array of 2 elements.
 */
function getWindowSize() {
    var windowSize = new Dimensions();
    if (navigator.appName == "Netscape") {
        windowSize.w = window.innerWidth;
        windowSize.h = window.innerHeight;

    } else if (navigator.appName == "Microsoft Internet Explorer") {
        windowSize.w = document.body.clientWidth;
        windowSize.h = document.body.clientHeight;
    }

    return windowSize;
};

/*
 * toCornerLoc(centerLoc, object=kanji)
 *      Given the coordinates for the center of the object, returns the 
 *      coordinates for the top-left corner of the object, which is used
 *      to lay it out.
 */
function toCornerLoc(centerLoc, object) {
    var lookupPlane = getLookupPlane();

    if (object == null) {
        var objectSize = getElementDimensions("pivotKanji");
    } else {
        var objectSize = getElemendDimensions(object);
    }

    var retVal = new Coordinates();
    retVal.x = Math.round(centerLoc.x - objectSize.w/2);
    retVal.y = Math.round(centerLoc.y - objectSize.h/2);
    
    return retVal;
};

/*
 * hasHistory()
 *      Returns true if there is a previous lookup state recorded.
 */
function hasHistory() {
    return (currentIndex > 0);
}

/*
 * hasFuture()
 *      Returns true if the user has browsed back from a lookup state.
 */
function hasFuture() {
    if (currentIndex == null) {
        return false;
    } else {
        return (currentIndex < g_historyStore.length - 1);
    }
}

/*
 * previousPivot()
 *      Fetches the previous pivot (if one exists) and redraws.
 */
function previousPivot() {
    if (hasHistory()) {
        currentIndex--;
        clearKanji();
        drawKanji();
        drawControls();
    }
};

/*
 * nextPivot()
 *      Fetches the next pivot (if one exists) and redraws.
 */
function nextPivot() {
    if (hasFuture()) {
        currentIndex++;
        clearKanji();
        drawKanji();
        drawControls();
    }
}

/*
 * ord()
 *      Returns the character code of a character.
 */
function ord(char) {
    return char.charCodeAt(0);
}

/*
 * chr(charCode)
 *      Returns the character indicated by the given character code. 
 */
 function chr(charCode) {
     return String.fromCharCode(charCode);
 }

var g_clearState = {
    'seeding':  clearSeedingInput,
    'lookup':   clearLookup,
}

var g_drawState = {
    'seeding':  drawSeedingInput,
    'lookup':   drawLookup,
}

var g_initState = {
    'seeding':  drawSeedingInput,
    'lookup':   initLookup,
}

function initInterface() {
    drawSeedingInput();
    callLater(4, function() { 
            if (emptyInput()) {
                drawError('Enter a kanji similar to',
                        'to the one you want to find.', 0);
            }
        });
}

function emptyInput() {
    return g_currentState == 'seeding' 
        && document['seedForm'].seedKanji.value == '';
}

/*
 *  Converts coordinates to a style string.
 */
function locToStyle(loc) {
    return "position:absolute; left:" + loc.x + "px; top:" + loc.y + "px; "; 
}

// Image rollover function.
function roll(imageName, imageSrc) {
    document[imageName].src = imageSrc;
}

