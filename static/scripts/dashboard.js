$(() => {
    const $assignments = $('#assignments');
    const $projects = $('#projects');
    const $materials = $('#materials');
    $assignments.attr('href', 'docs?category=assignment');
    $projects.attr('href', 'docs?category=project');
    $materials.attr('href', 'docs?category=material');

})
const user_id = '182414ec-63b4-4e70-b727-51cddbccb55a';
if (!localStorage.getItem('user_id') || localStorage.getItem('user_id') === 'null'){
    localStorage.setItem('user_id', user_id);
}
