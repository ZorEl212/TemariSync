$(document).ready(function () {
      $.ajax({
    url: "https://yeab.tech/temarisync/api/v1/checkuser",
    method: "GET",
    success: function (response, status, xhr) {
      if (xhr.status === 200) {
        console.log(response);
      }
    },
    error: function (xhr, status, error) {
        console.error(error);
        if (xhr.status === 401)
        {
            sessionStorage.removeItem("user_id");
            window.location.href = "login";
        }
    },
  });
  
    const $docs = $('#docs');
    const $searchTerm = $('#search');
    let docs;
    const user_id = sessionStorage.getItem('user_id');
    const category = new URLSearchParams(window.location.search).get('category');
    const filter = new URLSearchParams(window.location.search).get('filter');
    let url;

    if (filter === 'all') {
        url = 'https://yeab.tech/temarisync/api/v1/documents/all';
        $('#myDocs').text('All Documents');
    } else {
        url = 'https://yeab.tech/temarisync/api/v1/documents/' + user_id
        $('#myDocs').text(`My ${category.charAt(0).toUpperCase() + category.slice(1)}s`);
    }

    function createArticle(title, content, doc_id, user_id) {
        return `
        <article class="rounded-lg border border-gray-100 bg-white p-4 shadow-sm transition hover:shadow-lg sm:p-6">
            <span class="inline-block rounded bg-blue-600 p-2 text-white">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path d="M12 14l9-5-9-5-9 5 9 5z" />
                    <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222" />
                </svg>
            </span>
            <a href="#">
                <h3 class="mt-0.5 text-lg font-medium text-gray-900">${title}</h3>
            </a>
            <p class="mt-2 line-clamp-3 text-sm/relaxed text-gray-500">${content}</p>
            <a href="docfile?doc_id=${doc_id}&user_id=${user_id}" class="group mt-4 inline-flex items-center gap-1 text-sm font-medium text-blue-600">
                Find out more
                <span aria-hidden="true" class="block transition-all group-hover:ms-0.5 rtl:rotate-180">&rarr;</span>
            </a>
        </article>
        `;
    }

    function fetchDocuments() {
        $.ajax({
            type: 'GET',
            url: url,
            data: '{}',
            dataType: 'json',
            success: function (documents) {
                docs = documents;
                renderDocuments();
            }
        });
    }

    function renderDocuments() {
        const searchTerm = $searchTerm.val().toLowerCase();
        const articles = [];

        $.each(docs, function (i, document) {
            if (category === null) {
                if (document.hasOwnProperty('title') && document.hasOwnProperty('description')) {
                    if (document.title.toLowerCase().includes(searchTerm) || document.description.toLowerCase().includes(searchTerm)) {
                        articles.push(createArticle(document.title, document.description, document.id, user_id));
                    }
                }
            } else {
                if (document.hasOwnProperty('title') && document.hasOwnProperty('description')
                    && document.category.toLowerCase() === category.toLocaleLowerCase()) {
                    if (document.title.toLowerCase().includes(searchTerm) || document.description.toLowerCase().includes(searchTerm)) {
                        articles.push(createArticle(document.title, document.description, document.id, user_id));
                    }
                }
            }
        });
 
        // Clear the docs container and append all articles
        $docs.empty();
        for (let i = 0; i < articles.length; i++) {
            $docs.append(articles[i]);
        }
    }

    // Fetch documents initially
    fetchDocuments();

    // Re-render documents whenever the search term changes
    $searchTerm.on('input', renderDocuments);
});
