
const DRY_RUN = true;
const response = {};


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
const SCROLL_SIZE = 100;

let latest_post_reverse_index = 1
while (latest_post_reverse_index <= anchors_length()) {
    if (isLiked(latest_post_reverse_index)) {
        break;
    } else {
        latest_post_reverse_index++;
        anchors()[0].scrollIntoView();
        scrollbar.scrollTop -= SCROLL_SIZE;
        await new Promise(r => setTimeout(r, 1000));
    }
}

const unliked_post_start_index = anchors_length() - latest_post_reverse_index + 1;
response["links"] = anchors().slice(unliked_post_start_index).map(anchor => anchor.href.replace('https://www.instagram.com/reel/', 'https://www.instagram.com/p/'));
response["links_as_text"] = response["links"].join('\n') + '\n';
// TODO: prompt to save links_as_text to file (with datetime stamp) & copy it to clipboard

for (let i = unliked_post_start_index; i < anchors_length() && !DRY_RUN; i++) {
    const anchor = anchors()[i];
    doubleClickAtCoordinates(anchor);
    await new Promise(r => setTimeout(r, 1000));
    // index + reverse_index = length
    if (!isLiked(anchors_length() - i)) response["logs"] += `Failed to like index=${i} ${anchor.href}\n`;
}
// TODO: prompt to save logs to file (with datetime stamp) & copy it to clipboard
response