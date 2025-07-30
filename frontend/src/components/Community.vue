<script setup lang="ts">
import {
  Card,
  CardHeader,
  CardTitle,
  CardFooter,
  CardContent,
} from "@/components/ui/card";

import { Button } from "@/components/ui/button";

import DiscordIcon from "@/icons/DiscordIcon.vue";
</script>

<template>
  <section
    
    class="py-12"
  >
    <hr class="border-border" />
    <div class="py-20 sm:py-20">
      <div class="lg:w-[60%] mx-auto">
        <Card
          class="bg-background border-0 shadow-none text-center  flex flex-col "
        >
          <CardHeader>
            <CardTitle class="text-4xl md:text-5xl font-bold">
              <Component
                class="w-20 h-20 m-auto mb-4 "
                :is="DiscordIcon"
              />
              Ready to join this
              <span
                class="text-transparent bg-gradient-to-r from-[#D247BF] to-primary bg-clip-text"
              >
                Community?
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent class="lg:w-[80%] text-xl place-self-center text-muted-foreground">
            Join our vibrant Discord community! Connect, share, and grow with
            like-minded enthusiasts. Click to dive in! 🚀
          </CardContent>

          <CardFooter class="flex justify-center">
            <Button as-child>
              <a
                href="https://discord.com/"
                target="_blank"
              >
                Join Discord
              </a>
            </Button>
          </CardFooter>
        </Card>
      </div>
    </div>
    <hr class="border-border" />
  </section>
</template>
