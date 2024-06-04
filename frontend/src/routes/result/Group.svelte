<script lang="ts">
	import { ListBox, ListBoxItem, popup } from '@skeletonlabs/skeleton';
	import type { PopupSettings } from '@skeletonlabs/skeleton';

	export let comboboxValue: string;

	const popupCombobox: PopupSettings = {
		event: 'click',
		target: 'popupCombobox',
		placement: 'bottom',
		closeQuery: '.listbox-item'
	};
</script>

<div>
	<button class="btn bg-reddit text-base text-white w-28 justify-between" use:popup={popupCombobox}>
		<span class="capitalize">{comboboxValue ?? 'View by'}</span>
		<span>↓</span>
	</button>

	<div class="card w-48 text-base bg-reddit text-white shadow-xl py-2" data-popup="popupCombobox">
		<ListBox rounded="rounded-full m-1">
			<ListBoxItem
				bind:group={comboboxValue}
				name="view"
				value="month"
				active="bg-orange-400 text-white">Month</ListBoxItem
			>
			<ListBoxItem
				bind:group={comboboxValue}
				name="view"
				value="week"
				active="bg-orange-400 text-white">Week</ListBoxItem
			>
			<ListBoxItem
				bind:group={comboboxValue}
				name="view"
				value="year"
				active="bg-orange-400 text-white">Year</ListBoxItem
			>
		</ListBox>
		<div class="arrow bg-surface-100-800-token" />
	</div>
</div>
