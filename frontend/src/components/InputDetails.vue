<template>
    <section class="flex flex-col justify-center items-center flex-grow">
        <form class="flex flex-col space-y-4 w-1/4">
            <div class="flex flex-col">
                <label for="salary">salary (post tax)</label>
                <input class="p-2 border rounded" id="salary" type="number" placeholder="salary" />
            </div>

            <div class="flex flex-col">
                <label for="debt">debt</label>
                <input class="p-2 border rounded" id="debt" type="number" placeholder="debt" />
            </div>

            <div class="flex flex-col">
                <label for="bills">bills (average)</label>
                <input class="p-2 border rounded" id="bills" type="number" placeholder="bills" />
            </div>
        </form>

        <button class="cursor-poiner">view your finance breakdown</button>
    </section>
</template>
