$(() => {
    const $assignments = $('#assignments');
    const $projects = $('#projects');
    const $materials = $('#materials');
    $assignments.attr('href', 'docs?category=assignment');
    $projects.attr('href', 'docs?category=project');
    $materials.attr('href', 'docs?category=material');
    const $find = $('#find');

})
const user_id = 'bd4d3614-f2b0-4f34-b6a6-c6cff2af127e';
if (!localStorage.getItem('user_id') || localStorage.getItem('user_id') === 'null'){
    localStorage.setItem('user_id', user_id);
} else {
    user_id = localStorage.getItem('user_id');
}
