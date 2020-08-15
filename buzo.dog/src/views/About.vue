<template>
  <div class='about col-md-8 mx-auto my-4'>
    <h3>What is this site?</h3>
    <p>Buzo.dog is a no nonsense library of articles from a selection of publications spanning across culture, technology, science, phiosophy and general wisdom. This website has emerged out of <a href='https://thatgurjot.com/'>my</a> desire to teach myself the fundamentals of web development with Vuejs.</p>

    <h3>What can I do here?</h3>
    <p>A couple of things. You can 'Fetch' a cool link, or you can go for a 'Walk' and decide which link to follow. Buzo will be with you through it all, in spirit.</p>

    <h3>How legal is this?</h3>
    <p>Very little. By scraping the publications and storing their links and at times even the article text on my servers, I am infringing on their copyright. But this is a personal site entirely used by no one else. If you are a representative of one of these publications and would like your content taken down, just send me an email at contact (at) thatgurjot (dot) com.</p>

    <h3>This is a cool site. Can I help?</h3>
    <p>Sure! You can help me cover the cost of keeping this site up and for buying Buzo treats. (belly rubs cost extra)</p>
    <ul class='list-inline'>
      <li class='list-inline-item mb-2'>
        <a class="bmc-button" target="_blank" href="https://www.buymeacoffee.com/thatgurjot"><img src="https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg" alt="Buy me a Book"><span style="margin-left:5px;font-size:18px !important;">Foreign users</span></a>
      </li>
      <li class='list-inline-item mb-2'>
        <a class="bmc-button" target="_blank" style="background-color: #42b983" href="https://www.instamojo.com/@thatgurjot/"><img src="https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg" alt="Buy me a Book"><span style="margin-left:5px;font-size:18px !important;">Indian users</span></a>
      </li>
    </ul>

    <h3>Terms and Conditions</h3>
    <p>Buzo.dog is shared under a CC-BY-SA-4.0 license. The creators of this site are not liable for any content that you may access through this site. The creators claim no ownership over the content aggregated, displayed and accessed through this site. By using this site you are implicitly agreeing to these terms and conditions.
    </p>

    <h3>Who am I?</h3>
    <avatar
          avatarStyle='Circle'
          topType='Turban'
          hatColor='Black'
          accessoriesType='Prescription02'
          hairColor='Black'
          facialHairType='BeardMedium'
          facialHairColor='Black'
          clotheType='Hoodie'
          clotheColor='Black'
          eyeType='Default'
          eyebrowType='DefaultNatural'
          mouthType='Smile'
          skinColor='Brown'
        />
      <p class='text-muted'><a href='https://thatgurjot.com/'>Mysterious Turban Man</a></p>
  </div>
</template>

<script>
import { ReactInVue } from 'vuera'
import Avatar from 'avataaars'

export default {
  name: 'About',
  components: {
    'avatar': ReactInVue(Avatar)
  }
}
</script>

<style scoped>
.bmc-button img{height: 34px !important;width: 35px !important;margin-bottom: 1px !important;box-shadow: none !important;border: none !important;vertical-align: middle !important;}.bmc-button{padding: 7px 15px 7px 10px !important;line-height: 35px !important;height:51px !important;text-decoration: none !important;display:inline-flex !important;color:#ffffff !important;background-color:#FF813F;border-radius: 5px !important;border: 1px solid transparent !important;padding: 7px 15px 7px 10px !important;font-size: 28px !important;letter-spacing:0.6px !important;box-shadow: 0px 1px 2px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;margin: 0 auto !important;-webkit-box-sizing: border-box !important;box-sizing: border-box !important;}.bmc-button:hover, .bmc-button:active, .bmc-button:focus {-webkit-box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;text-decoration: none !important;box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;opacity: 0.85 !important;color:#ffffff !important;}

a {
  text-decoration: none;
  color: black;
}
</style>