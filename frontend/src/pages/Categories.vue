<script setup lang="ts">

</script>



<template>
    
        <section class="w-[90%] 2xl:w-[75%] mx-auto py-12 md:py-20">            
                
                    <div class="mx-auto max-w-2xl lg:max-w-none">
                        <h2 class="text-2xl font-bold ">Games</h2>

                        <div class="mt-6 space-y-12 lg:grid lg:grid-cols-3 lg:space-y-0 lg:gap-x-6">
                            <div class="group relative">
                                <img src="/images/poe2.jpg"
                                    alt="Desk with leather desk pad, walnut desk organizer, wireless keyboard and mouse, and porcelain mug."
                                    class="w-full rounded-lg bg-white object-cover object-left group-hover:opacity-75 max-sm:h-80 sm:aspect-2/1 lg:aspect-square" />
                                <h3 class="mt-6 text-sm ">
                                   <router-link :to="{ name: 'catalog', params: { gameSlug: 'path-of-exile-2' }, query: { category: 'all' } }">
                                    Path of Exile 2
                                    </router-link>
                                </h3>
                                <p class="text-base font-semibold ">Currency and items</p>
                            </div>
                            <div class="group relative">
                                <img src="/images/d4.png"
                                    alt="Wood table with porcelain mug, leather journal, brass pen, leather key ring, and a houseplant."
                                    class="w-full rounded-lg bg-white object-cover object-right group-hover:opacity-75 max-sm:h-80 sm:aspect-2/1 lg:aspect-square" />
                                <h3 class="mt-6 text-sm ">
                                    <router-link :to="{ name: 'catalog', params: { gameSlug: 'diablo-4' }, query: { category: 'all' } }">
                                        Diablo 4
                                        </router-link>
                                </h3>
                                <p class="text-base font-semibold ">Gold and best gear</p>
                            </div>
                            <div class="group relative">
                                <img src="/images/d2.jpg"
                                    alt="Collection of four insulated travel bottles on wooden shelf."
                                    class="w-full rounded-lg bg-white object-cover group-hover:opacity-75 max-sm:h-80 sm:aspect-2/1 lg:aspect-square" />
                                <h3 class="mt-6 text-sm ">
                                    <router-link :to="{ name: 'catalog', params: { gameSlug: 'destiny-2' }, query: { category: 'all' } }">
                                            Destiny 2
                                            </router-link>
                                </h3>
                                <p class="text-base font-semibold ">Pve and Pvp</p>
                            </div>
                        </div>
                    </div>               
            
        </section>
    
</template>