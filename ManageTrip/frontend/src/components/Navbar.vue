<template>
  <nav>
    <div>
      <router-link :to="{ name: 'home' }"
        >QuestionTime
      </router-link>

      <div>
        <ul>
          <li>
            <router-link
              :to="{ name: 'trip-editor' }"
              :params="{ slug: undefined }"
              >Ask Question
            </router-link>
          </li>
          <li>
            <a  href="/accounts/logout/"
              >Logout
            </a>
          </li>
          <li>
            {{ login_user }}

          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavbarComponent",
  props:{
    
    login_user:{
      type:String,
      required:true
    }
  }
};
</script>