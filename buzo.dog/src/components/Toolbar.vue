<template>
    <div class="sp-floating-icons">
        <ul v-if="reader" class="list-unstyled">
            <li style=" width: 25%">
                <button id='toggle-text-view' class='btn btn-success' @click="$emit('toggle')">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.5 3H3V6.5H4V4H6.5V3Z" fill="currentColor" /><path d="M8.5 4V3H11V4H8.5Z" fill="currentColor" /><path d="M13 4H15.5V3H13V4Z" fill="currentColor" /><path d="M17.5 3V4H20V6.5H21V3H17.5Z" fill="currentColor" /><path d="M21 8.5H20V11H21V8.5Z" fill="currentColor" /><path d="M21 13H20V15.5H21V13Z" fill="currentColor" /><path d="M21 17.5H20V20H17.5V21H21V17.5Z" fill="currentColor" /><path d="M15.5 21V20H13V21H15.5Z" fill="currentColor" /><path d="M11 21V20H8.5V21H11Z" fill="currentColor" /><path d="M6.5 21V20H4V17.5H3V21H6.5Z" fill="currentColor" /><path d="M3 15.5H4V13H3V15.5Z" fill="currentColor" /><path d="M3 11H4V8.5H3V11Z" fill="currentColor" /><path d="M11 9.5H7V7.5H17V9.5H13V16.5H11V9.5Z" fill="currentColor" /></svg>
                </button>
            </li>
            <li style=" width: 25%">
                <button id='show-internal-links' class='btn btn-warning' @click="$emit('links')">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14.8284 12L16.2426 13.4142L19.071 10.5858C20.6331 9.02365 20.6331 6.49099 19.071 4.9289C17.509 3.3668 14.9763 3.3668 13.4142 4.9289L10.5858 7.75732L12 9.17154L14.8284 6.34311C15.6095 5.56206 16.8758 5.56206 17.6568 6.34311C18.4379 7.12416 18.4379 8.39049 17.6568 9.17154L14.8284 12Z" fill="currentColor" /><path d="M12 14.8285L13.4142 16.2427L10.5858 19.0711C9.02372 20.6332 6.49106 20.6332 4.92896 19.0711C3.36686 17.509 3.36686 14.9764 4.92896 13.4143L7.75739 10.5858L9.1716 12L6.34317 14.8285C5.56212 15.6095 5.56212 16.8758 6.34317 17.6569C7.12422 18.4379 8.39055 18.4379 9.1716 17.6569L12 14.8285Z" fill="currentColor" /><path d="M14.8285 10.5857C15.219 10.1952 15.219 9.56199 14.8285 9.17147C14.4379 8.78094 13.8048 8.78094 13.4142 9.17147L9.1716 13.4141C8.78107 13.8046 8.78107 14.4378 9.1716 14.8283C9.56212 15.2188 10.1953 15.2188 10.5858 14.8283L14.8285 10.5857Z" fill="currentColor" /></svg>
                </button>
            </li>
            <li v-if="isLoggedIn" style=" width: 25%" data-toggle="modal" data-target="#edit-modal" @click="$emit('modal')">
                <button id='edit-item' class='btn btn-danger'>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M21.2635 2.29289C20.873 1.90237 20.2398 1.90237 19.8493 2.29289L18.9769 3.16525C17.8618 2.63254 16.4857 2.82801 15.5621 3.75165L4.95549 14.3582L10.6123 20.0151L21.2189 9.4085C22.1426 8.48486 22.338 7.1088 21.8053 5.99367L22.6777 5.12132C23.0682 4.7308 23.0682 4.09763 22.6777 3.70711L21.2635 2.29289ZM16.9955 10.8035L10.6123 17.1867L7.78392 14.3582L14.1671 7.9751L16.9955 10.8035ZM18.8138 8.98525L19.8047 7.99429C20.1953 7.60376 20.1953 6.9706 19.8047 6.58007L18.3905 5.16586C18 4.77534 17.3668 4.77534 16.9763 5.16586L15.9853 6.15683L18.8138 8.98525Z" fill="currentColor" /><path d="M2 22.9502L4.12171 15.1717L9.77817 20.8289L2 22.9502Z" fill="currentColor" /></svg>
                </button>
            </li>
            <li style=" width: 25%" @click="scrollUp()">
                <button id='scroll-up' class='btn btn-secondary' >
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M17.6569 11.2929L16.2427 12.7071L12 8.46444L7.75735 12.7071L6.34314 11.2929L12 5.63605L17.6569 11.2929Z" fill="currentColor" /><path d="M17.6569 16.9497L16.2427 18.3639L12 14.1213L7.75735 18.364L6.34314 16.9498L12 11.2929L17.6569 16.9497Z" fill="currentColor" /></svg>
                </button>
            </li>
        </ul>
        <ul v-else class="list-unstyled">
            <li style="width: 25%" class="py-1" @click="$emit('toggle')">
                <button id='toggle-list-view' class='btn btn-primary'>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M20 4H4C3.44771 4 3 4.44772 3 5V19C3 19.5523 3.44772 20 4 20H20C20.5523 20 21 19.5523 21 19V5C21 4.44771 20.5523 4 20 4ZM4 2C2.34315 2 1 3.34315 1 5V19C1 20.6569 2.34315 22 4 22H20C21.6569 22 23 20.6569 23 19V5C23 3.34315 21.6569 2 20 2H4ZM6 7H8V9H6V7ZM11 7C10.4477 7 10 7.44772 10 8C10 8.55228 10.4477 9 11 9H17C17.5523 9 18 8.55228 18 8C18 7.44772 17.5523 7 17 7H11ZM8 11H6V13H8V11ZM10 12C10 11.4477 10.4477 11 11 11H17C17.5523 11 18 11.4477 18 12C18 12.5523 17.5523 13 17 13H11C10.4477 13 10 12.5523 10 12ZM8 15H6V17H8V15ZM10 16C10 15.4477 10.4477 15 11 15H17C17.5523 15 18 15.4477 18 16C18 16.5523 17.5523 17 17 17H11C10.4477 17 10 16.5523 10 16Z" fill="currentColor" /></svg>
                </button>
            </li>
            <li style="width: 25%" @click="scrollUp()">
                <button id='scroll-up' class='btn btn-secondary'>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M17.6569 11.2929L16.2427 12.7071L12 8.46444L7.75735 12.7071L6.34314 11.2929L12 5.63605L17.6569 11.2929Z" fill="currentColor" /><path d="M17.6569 16.9497L16.2427 18.3639L12 14.1213L7.75735 18.364L6.34314 16.9498L12 11.2929L17.6569 16.9497Z" fill="currentColor" /></svg>
                </button>
            </li>
        </ul>
    </div>
</template>

<script>
import $ from 'jquery';

export default {
    name: "Toolbar",
    components: {
    },
    data() {
      return {
        isLoggedIn: true,
        card: true
      };
    },
    props: ["reader"],
    methods: {
        scrollUp() {
            $([document.documentElement, document.body]).animate({
                scrollTop: $("#app").offset().top
            }, 1000);
        },
    }
}
</script>

<style scoped>
.sp-floating-icons {
	position: fixed;
	left: 0;
	z-index: 100;
}
@media screen and (max-width: 768px) {
    .sp-floating-icons {
        width: 100%;
        top: auto;
        bottom: -3px;
        transform: scale(.85);
    }
    .sp-floating-icons ul li:first-child {
        margin-left: 0px;
    }
    .sp-floating-icons ul li {
        display: inline-block;
        margin-left: -2px;
        margin-right: -2px;
    }
    .sp-floating-icons ul li button {
        width: 100%;
        display: block;
        text-align: center;
        height: 45px;
        padding-top: 12px;
    }
}
@media screen and (min-width: 769px) {
    .sp-floating-icons {
        top: 25%;
    }
    .sp-floating-icons ul li button {
        width: 50px;
        height: 50px;
    }
}
.list-unstyled {
	padding-left: 0;
	list-style: none;
}
.sp-floating-icons ul {
	margin-bottom: 0px;
}
</style>