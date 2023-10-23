
const DRY_RUN = true;
const response = {logs: '', errors: '', links: [], links_as_text: ''};


const anchors = () => Array.from(document.querySelectorAll('a[aria-label="Preview"]'))
const anchors_length = () => anchors().length
const isLiked = (reverse_index) => [...anchors()
    .find((_, index, array) => index === array.length - reverse_index)
    .closest('div[role="button"][aria-label="Double tap to like"]')
    .querySelectorAll('span')].find(span => span.textContent === '❤️');

const doubleClickAtCoordinates = (element, x=0, y=0) => {
    // Get the bounding rectangle of the element
    const rect = element.getBoundingClientRect();

    // Calculate the absolute coordinates within the viewport
    const absoluteX = rect.left + x;
    const absoluteY = rect.top + y;

    // Create a new MouseEvent with the appropriate properties
    const clickEvent = new MouseEvent('dblclick', {
        bubbles: true, cancelable: true, view: window, clientX: absoluteX, clientY: absoluteY,
    });

    // Dispatch the click event on the element
    element.dispatchEvent(clickEvent);
}

/** test index **/
// for (let i = 0; i < anchors_length(); i++) {
//     if (ancestor(anchors_length() - i).querySelectorAll(':scope a[aria-label="Preview"]')[0].href !== anchors()[i].href) throw new Error('Ancestor is not the same as anchor');
// }


const scrollbar = [...document.querySelectorAll('div[aria-label*="Messages in conversation with"] *')]
    .find(child => {
        const computedStyle = window.getComputedStyle(child);
        return computedStyle.getPropertyValue('overflow-y') === 'scroll';
    });

const save_file = (filename, text) => {
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

const format_date = () => new Date().toISOString().replaceAll(":", "-");


const SCROLL_SIZE = 400;
let latest_post_reverse_index = 1

const start = new Date();
while (true) {
    while (!(latest_post_reverse_index <= anchors_length())) {
        scrollbar.scrollTop -= SCROLL_SIZE;
        await new Promise(r => setTimeout(r, 0));
    }
    console.log(`latest_post_reverse_index=${latest_post_reverse_index} anchors_length()=${anchors_length()}`);
    if (isLiked(latest_post_reverse_index)) {
        break;
    } else {
        latest_post_reverse_index++;
    }
}
const end = new Date();
[`took ${end - start} ms latest_post_reverse_index=${latest_post_reverse_index}`].forEach(line => {
    console.log(line);
    response["logs"] += line + '\n';
});

const unliked_post_start_index = anchors_length() - latest_post_reverse_index + 1;
response["links"] = anchors().slice(unliked_post_start_index).map(anchor => anchor.href.replace('https://www.instagram.com/reel/', 'https://www.instagram.com/p/'));
response["links_as_text"] = response["links"].join('\n') + '\n';


// save_file(`links_as_text_${format_date()}.txt`, response["links_as_text"]);

for (let i = unliked_post_start_index; i < anchors_length() && !DRY_RUN; i++) {
    const anchor = anchors()[i];
    doubleClickAtCoordinates(anchor);
    await new Promise(r => setTimeout(r, 1000));
    // index + reverse_index = length
    if (!isLiked(anchors_length() - i)) response["errors"] += `Failed to like index=${i} ${anchor.href}\n`;
}

// save_file(`logs_${format_date()}.txt`, response["logs"]);

if (response["errors"] && response["errors"].length > 0) {
    // save_file(`errors_${format_date()}.txt`, response["errors"]);
}
localStorage.setItem('response', JSON.stringify(response));

/** no longer needed **/
// alert('Saving files'); // to handle losing focus when pasting into clipboard
// navigator.clipboard.writeText(response["links_as_text"]);
// navigator.clipboard.writeText(response["logs"]);
// navigator.clipboard.writeText(response["errors"]);
