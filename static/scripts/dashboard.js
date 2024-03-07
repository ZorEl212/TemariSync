$(() => {
    const $assignments = $('#assignments');
    const $projects = $('#projects');
    const $materials = $('#materials');


    $assignments.attr('href', 'docs?category=assignment');
    $projects.attr('href', 'docs?category=project');
    $materials.attr('href', 'docs?category=material');

})