const anchors = () => Array.from(document.querySelectorAll('a[aria-label="Preview"]'))
const anchors_length = () => anchors().length
const is_liked = (reverse_index) => [...anchors()
    .find((_, index, array) => index === array.length - reverse_index)
    .closest('div[role="button"][aria-label="Double tap to like"]')
    .querySelectorAll('span')].find(span => span.textContent === '❤️');

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
    if (is_liked(latest_post_reverse_index)) {
        break;
    }
    else {
        latest_post_reverse_index++;
        anchors()[0].scrollIntoView();
        scrollbar.scrollTop -= SCROLL_SIZE;
        await new Promise(r => setTimeout(r, 1000));
    }
}

const unliked_post_start_index = anchors_length() - latest_post_reverse_index + 1;
const response = {};
response["links_backup"] = anchors().slice(unliked_post_start_index).map(anchor => anchor.href);

anchors().slice(unliked_post_start_index).forEach(anchor => {

});