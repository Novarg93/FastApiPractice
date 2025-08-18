<script setup lang="ts">
import DefaultLayout from '@/layouts/DefaultLayout.vue';
import Hero from '@/components/Hero.vue';
import Benefits from '@/components/Benefits.vue';
import Features from '@/components/Features.vue';
import Services from '@/components/Services.vue';
import HowItWorks from '@/components/HowItWorks.vue';
import Testimonials from '@/components/Testimonials.vue';
import Team from '@/components/Team.vue';
import Community from '@/components/Community.vue';
import Pricing from '@/components/Pricing.vue';
import Contact from '@/components/Contact.vue';
import FAQ from '@/components/FAQ.vue'
import Categories from './Categories.vue';


</script>

<template>
  
   <DefaultLayout>
    <Categories/>
    <Benefits/>
    <Features/>
    <Services/>
    <HowItWorks/>
    <Testimonials/>
    <Team/>
    <Community/>
    <Pricing/>
    <Contact/>
    <FAQ/>
   </DefaultLayout> 
  
</template>